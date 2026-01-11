import json
from typing import List

from zentralbibliothek.models.networkrequest import NetworkRequest

from .smtpresponse import SmtpResponse


class SmtpRequest(NetworkRequest):
    """
    A class that represents an SmtpRequest.
    """

    def __init__(
        self,
        req_fqdn: str,
        zone_fqdn: str,
        remote_addr: str,
        mail_from: str,
        rcpt_tos: List[str],
        data: str,
    ):
        """
        Constructor for an SmtpRequest
        """
        super().__init__(
            req_fqdn=req_fqdn,
            zone_fqdn=zone_fqdn,
            protocol="SMTP",
            remote_addr=remote_addr,
        )
        self.mail_from = mail_from
        self.rcpt_tos = rcpt_tos
        self.data = data

    def __str__(self):
        return f"SMTP request from {self.mail_from} to {self.rcpt_tos}"

    @property
    def summary(self):
        return f"SMTP FROM:{self.mail_from} TO:{self.rcpt_tos[0] if self.rcpt_tos else 'none'}"

    @property
    def json(self):
        return json.dumps(
            {"mail_from": self.mail_from, "rcpt_tos": self.rcpt_tos, "data": self.data}
        )

    @property
    def default_response(self):
        """
        Returns a default SmtpResponse.
        The default is "250 OK".
        """
        return SmtpResponse(code=250, message="OK")
