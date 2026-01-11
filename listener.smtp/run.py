import asyncio
import logging
import os
import ssl
import sys

from aiosmtpd.controller import Controller
from smtphandler import SmtpHandler
from zentralbibliothek.dbclient3 import DatabaseClient
from zentralbibliothek.utils import Utils

logger = logging.getLogger("listener.smtp")


def check_privileges(port):
    """
    Checks if root privileges are needed and if they are present.
    """
    if port < 1024 and os.geteuid() != 0:
        logger.error(
            f"Listening on port {port} requires root privileges. Skipping port."
        )
        return False
    return True


def main():
    Utils.banner()

    db = DatabaseClient.get_instance()
    if db.test_connectivity() == False:
        logger.critical("db connection failed")
        return -1

    logger.info("db connected")

    # --- Port Configuration ---
    iface: str = str(os.getenv("LSTNER_SMTP_INTERFACE", "0.0.0.0"))

    # Port 25 (Standard SMTP)
    port_smtp: int = int(os.getenv("LSTNER_SMTP_PORT", 25))
    # Port 587 (Submission)
    port_submission: int = int(os.getenv("LSTNER_SMTP_SUBMISSION_PORT", 587))
    # Port 465 (SMTPS / SSL)
    port_smtps: int = int(os.getenv("LSTNER_SMTP_SSL_PORT", 465))

    # --- SSL Cert for SMTPS (Port 465) ---
    cert_file = os.environ.get("DSSLDRF_TLS_CRT_FILE", None)
    key_file = os.environ.get("DSSLDRF_TLS_KEY_FILE", None)

    ssl_context = None

    # Check if the specified certificate files exist
    if not (os.path.exists(cert_file) and os.path.exists(key_file)):
        logger.critical(f"Certificate files not found: {cert_file} or {key_file}")
        logger.critical(f"Port {port_smtps} (SMTPS) will be disabled.")
    else:
        # Try to load the specified certificate
        try:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(cert_file, key_file)
            logger.info(f"SSL context created successfully from {cert_file}.")
        except Exception as e:
            logger.error(
                f"Failed to load SSL context from {cert_file}. Port {port_smtps} (SMTPS) will be disabled. Error: {e}"
            )
            ssl_context = None  # Ensure it's disabled if loading fails

    # --- Create Handler and Controllers ---
    handler = SmtpHandler()
    controllers = []

    # Controller for Port 25 (SMTP)
    if check_privileges(port_smtp):
        controller_smtp = Controller(handler, hostname=iface, port=port_smtp)
        controllers.append(("SMTP", port_smtp, controller_smtp))

    # Controller for Port 587 (Submission)
    if check_privileges(port_submission):
        controller_submission = Controller(
            handler, hostname=iface, port=port_submission
        )
        controllers.append(("Submission", port_submission, controller_submission))

    # Controller for Port 465 (SMTPS)
    # Only start if ssl_context was successfully loaded
    if ssl_context and check_privileges(port_smtps):
        controller_smtps = Controller(
            handler,
            hostname=iface,
            port=port_smtps,
            ssl_context=ssl_context,  # Enable implicit SSL
        )
        controllers.append(("SMTPS", port_smtps, controller_smtps))

    if not controllers:
        logger.critical(
            "No SMTP ports are configured or privilege checks failed. Exiting."
        )
        return -1

    try:
        # Start all controllers
        for name, port, controller in controllers:
            controller.start()
            logger.info(f"{name} listener started on {iface}:{port}/tcp")

        logger.info("All listeners started. Press Ctrl+C to stop.")
        loop = asyncio.get_event_loop()
        loop.run_forever()

    except KeyboardInterrupt:
        logger.info("Stopping listeners...")
    except Exception as ex:
        logging.exception(ex)
        return -1
    finally:
        # Stop all controllers
        for name, port, controller in controllers:
            if controller.is_serving:
                controller.stop()
                logger.info(f"{name} listener on port {port} stopped.")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as ex:
        logging.exception(ex)
        sys.exit(1)
