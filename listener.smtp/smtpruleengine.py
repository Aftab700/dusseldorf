import re

from models.smtprequest import SmtpRequest
from models.smtpresponse import SmtpResponse
from zentralbibliothek.ruleengine import Predicate, Result, RuleEngine

# region predicates


class SmtpMailFromPredicate(Predicate):
    """
    Check if the MAIL FROM address matches a regex.
    Parameter: a regex string.
    """

    @classmethod
    def satisfied_by(cls, request: SmtpRequest, parameter: str):
        if not parameter:
            return True
        return re.search(parameter, request.mail_from, re.IGNORECASE) is not None


class SmtpRcptToPredicate(Predicate):
    """
    Check if *any* RCPT TO address matches a regex.
    Parameter: a regex string.
    """

    @classmethod
    def satisfied_by(cls, request: SmtpRequest, parameter: str):
        if not parameter:
            return True
        for rcpt in request.rcpt_tos:
            if re.search(parameter, rcpt, re.IGNORECASE):
                return True
        return False


class SmtpDataContainsPredicate(Predicate):
    """
    Check if the email body (data) contains a regex match.
    Parameter: a regex string.
    """

    @classmethod
    def satisfied_by(cls, request: SmtpRequest, parameter: str):
        if not parameter:
            return True
        # Using re.DOTALL to make '.' match newlines
        return re.search(parameter, request.data, re.IGNORECASE | re.DOTALL) is not None


# endregion

# region results


class SetSmtpResponseCodeResult(Result):
    """
    Sets the response code (e.g., 250, 550, 421) of the SMTP response.
    Parameter: The integer code as a string (e.g., "550").
    """

    @classmethod
    def execute(cls, result_data: dict, parameter: str):
        response: SmtpResponse = result_data["response"]
        try:
            response.code = int(parameter)
        except ValueError:
            pass  # Keep default if parameter is invalid
        result_data["response"] = response
        return result_data


class SetSmtpResponseMessageResult(Result):
    """
    Sets the response message of the SMTP response.
    Parameter: The message string (e.g., "User unknown").
    """

    @classmethod
    def execute(cls, result_data: dict, parameter: str):
        response: SmtpResponse = result_data["response"]
        response.message = parameter
        result_data["response"] = response
        return result_data


# endregion


# this method is called from the handler.
def get_response(request: SmtpRequest) -> SmtpResponse:
    """
    Maps the "keys" in the DB to the classes defined above
    and calls the main rule engine.
    """
    predicate_mappings: dict = {
        "smtp.from": SmtpMailFromPredicate,
        "smtp.to": SmtpRcptToPredicate,
        "smtp.data.contains": SmtpDataContainsPredicate,
    }
    result_mappings: dict = {
        "smtp.response.code": SetSmtpResponseCodeResult,
        "smtp.response.message": SetSmtpResponseMessageResult,
    }

    # Call the core rule engine
    return RuleEngine.get_response_from_request(
        request, predicate_mappings, result_mappings
    )
