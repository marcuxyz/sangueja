import os

import httpx
from app.http.client import HttpClient


class Whatsapp:
    def __init__(self, url: str = None):
        self.client = url or HttpClient(os.environ["WHATSAPP_URL"])

    def send_notification(self, message: str) -> bool:
        """Send a text notification through the configured WhatsApp client.

        Args:
            message: Text to send in the notification.

        Returns:
            True when WhatsApp responds with HTTP status 200.

        Raises:
            RuntimeError: If the WhatsApp request fails.
        """
        headers = self.headers()
        params = self.params(message=message)

        try:
            response = self.client.send(headers=headers, params=params)
            if response.status_code == 200:
                return True
        except httpx.HTTPError as error:
            raise RuntimeError(f"failed to connect a whatsapp #{error}") from error

    def headers(self) -> dict:
        """Build the headers required by the WhatsApp API.

        Returns:
            A dictionary containing the content type, accepted format, and API token.
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'token': os.environ["WHATSAPP_TOKEN"]
        }
        return headers

    def params(self, message: str) -> dict:
        """Build the parameters required to send a WhatsApp message.

        Args:
            message: Text to send.

        Returns:
            A dictionary containing the recipient number and message text.
        """
        return {
            "number": os.environ["WHATSAPP_NUMBER"],
            "text": message
        }
