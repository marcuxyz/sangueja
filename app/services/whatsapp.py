import os

import httpx
from app.http.client import HttpClient


class Whatsapp:
    def __init__(self, url: str = None):
        self.WHATSAPP_URL = os.environ["WHATSAPP_URL"]
        self.WHATSAPP_TOKEN = os.environ["WHATSAPP_TOKEN"]
        self.WHATSAPP_NUMBER = os.environ["WHATSAPP_NUMBER"]
        self.client = HttpClient(self.WHATSAPP_URL or url)

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
        data = self.payload(message=message)

        try:
            response = self.client.send(headers=headers, data=data)
            return response.status_code == 200
        except httpx.HTTPError as error:
            raise RuntimeError(f"failed to connect a whatsapp #{error}") from error

    def headers(self) -> dict:
        """Build the headers required by the WhatsApp API.

        Returns:
            A dictionary containing the content type, accepted format, and API token.
        """
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "token": self.WHATSAPP_TOKEN,
        }

    def payload(self, message: str) -> dict:
        """Build the parameters required to send a WhatsApp message.

        Args:
            message: Text to send.

        Returns:
            A dictionary containing the recipient number and message text.
        """
        return {
            "number": self.WHATSAPP_NUMBER,
            "text": message,
        }
