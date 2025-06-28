from app import errors
from app import settings
from app.fake import fake_secondary_external_api
from .base import BaseSmsProvider

class SecondarySmsApiProvider(BaseSmsProvider):
    """Secondary SMS API Provider"""

    API_TOKEN = settings.SECONDARY_API_KEY

    def _validate_set_recipient(self, *args):
        """Validate recipient (secondary: must be 9 digits, only digits)."""
        if not args or not args[0]:
            raise errors.InvalidRecipientException("Recipient is required")
        phone = str(args[0])
        # Secondary: must be exactly 9 digits, only digits
        if not (phone.isdigit() and len(phone) == 9):
            raise errors.InvalidRecipientException("Recipient must be exactly 9 digits")

    def _validate_set_content(self, *args):
        """Validate content (secondary: max 70 chars)."""
        if not args or not args[0]:
            raise errors.InvalidContentException("Content is required")
        content = str(args[0])
        if len(content) > 70:
            raise errors.InvalidContentException("Content too long for secondary provider")

    def _validate_before_sending(self):
        """Check if content and recipient are set."""
        if not self.recipient:
            raise errors.RecipientNotSet("Recipient not set")
        if not self.content:
            raise errors.ContentNotSet("Content not set") 

    def _process_response(self, resp):
        """Check response content. Return (boolean, resp)"""
        # Success if resp.get("status") == "OK"
        if resp.get("status") == "OK":
            return True, resp
        return False, resp

    def _prepare_payload(self):
        """Construct and return payload for secondary API."""
        return {
            "auth_key": self.API_TOKEN,
            "sender": self.SENDER_NAME,
            "number": self.recipient,
            "text": self.content,
        }

    def send(self):
        """Send the message using the secondary API."""
        self._validate_before_sending()
        payload = self._prepare_payload()
        response = fake_secondary_external_api(payload)
        return self._process_response(response)