import json

from zentralbibliothek.models.networkresponse import NetworkResponse


class SmtpResponse(NetworkResponse):
    """A basic SMTP response"""

    def __init__(self, code: int = 250, message: str = "OK"):
        self.code = code
        self.message = message

    @property
    def summary(self):
        """Display the SmtpResponse as a string"""
        return f"{self.code} {self.message}"

    def __str__(self):
        return self.summary

    @property
    def json(self):
        return json.dumps({"code": self.code, "message": self.message})
