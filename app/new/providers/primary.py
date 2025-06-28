from app import errors
from app import settings
from app.fake import fake_primary_external_api
from .base import BaseSmsProvider


class PrimarySmsApiProvider(BaseSmsProvider):
    """Primary SMS API Provider"""

    API_KEY = settings.PRIMARY_API_KEY

    def _validate_set_recipient(self, *args):
        """Validate recipient using the same logic as defined in `old.py` file."""
        if not args or not args[0]:
            raise errors.InvalidRecipientException("Recipient is required")
        phone = str(args[0])
        if not phone.isdigit() or len(phone) < 9:
            raise errors.InvalidRecipientException("Invalid recipient phone number")

    def _validate_set_content(self, *args):
        """Validate content."""
        if not args or not args[0]:
            raise errors.InvalidContentException("Content is required")
        content = str(args[0])
        if len(content) > 160:
            raise errors.InvalidContentException("Content too long")

    def _validate_before_sending(self):
        """Check if content and recipient are set."""
        if not self.recipient:
            raise errors.RecipientNotSet("Recipient not set")
        if not self.content:
            raise errors.ContentNotSet("Content not set") 

    def _process_response(self, resp):
        """Check response content. Return (boolean, resp)"""
        if resp.get("status") == "SENT":
            return True, resp
        return False, resp

    def _prepare_payload(self):
        """Construct and return payload."""
        return {
            "api_key": self.API_KEY,
            "from": self.SENDER_NAME,
            "phone": self.recipient,  # <-- changed from "to" to "phone"
            "message": self.content,
        }

    def send(self):
        """Send the message"""
        self._validate_before_sending()
        payload = self._prepare_payload()
        response = fake_primary_external_api(payload)
        return self._process_response(response)
