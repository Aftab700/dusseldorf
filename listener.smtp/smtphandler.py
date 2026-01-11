import logging
import time

from models.smtprequest import SmtpRequest
from smtpruleengine import get_response
from zentralbibliothek.dbclient3 import DatabaseClient

logger = logging.getLogger(__name__)


class SmtpHandler:
    """
    This class handles incoming SMTP connections and data.
    It's the equivalent of the DusseldorfResolver for DNS.
    """

    def __init__(self):
        self.db = DatabaseClient.get_instance()
        logger.info("SmtpHandler initialized.")

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        """
        This is called for each 'RCPT TO:' command.
        We check if the recipient domain is a zone we manage.
        """
        try:
            domain = address.split("@")[1]
        except IndexError:
            logger.warning(f"Invalid RCPT TO address: {address}")
            return "501 Invalid address"

        # Check if the domain is valid and if we have a zone for it
        # This mirrors the domain/zone check in DusseldorfResolver
        zone_fqdn = self.db.find_zone_for_request(domain)

        if zone_fqdn is None:
            logger.debug(f"Denying relay for {address} (no zone found)")
            return "550 Relay access denied"

        # If the zone exists, accept the recipient
        logger.debug(f"Accepting RCPT TO:{address} for zone {zone_fqdn}")
        envelope.rcpt_tos.append(address)
        return "250 OK"

    async def handle_DATA(self, server, session, envelope):
        """
        This is called after the client sends 'DATA' and the email body.
        This is where we run the rule engine.
        """
        start_of_request = time.perf_counter()

        client_ip = session.peer[0]
        mail_from = envelope.mail_from
        rcpt_tos = envelope.rcpt_tos

        # We need to pick one FQDN/Zone to pass to the NetworkRequest
        # We'll pick the first valid recipient
        try:
            primary_rcpt = rcpt_tos[0]
            request_fqdn = primary_rcpt.split("@")[1]
            zone_fqdn = self.db.find_zone_for_request(request_fqdn)
        except Exception:
            logger.error("Could not determine FQDN or Zone from recipients, skipping.")
            return "500 Internal server error"

        # Decode data, replacing errors
        data = envelope.content.decode("utf-8", errors="replace")

        # Create the SmtpRequest object
        req = SmtpRequest(
            req_fqdn=request_fqdn,
            zone_fqdn=zone_fqdn,
            remote_addr=client_ip,
            mail_from=mail_from,
            rcpt_tos=rcpt_tos,
            data=data,
        )

        # Get the response from the rule engine
        # This will return a default SmtpResponse if no rules match
        response = get_response(req)

        if response is None:
            logger.error(f"no response found for {req.summary}")
            return "500 Internal server error"

        end_of_request = time.perf_counter()

        # Log the interaction
        start_db_write = time.perf_counter()
        self.db.save_interaction(req, response)
        end_db_write = time.perf_counter()

        request_time = round(end_of_request - start_of_request, 6)
        db_write_time = round(end_db_write - start_db_write, 6)
        logger.debug(
            "SMTPHandler resp: %.3f s, DB write: %.3f s", request_time, db_write_time
        )

        # Return the final response code and message
        return f"{response.code} {response.message}"
