import os
import httpx


class HttpClient:
    """Responsible for connect server with http

    Args:
        url (str, optional): Pass the URL to connect via HTTP protocol. Defaults to None.
    """

    def __init__(self, url: str = None):
        self.url = url

    def client(self):
        return httpx.Client(timeout=self.timeout())

    def timeout(self):
        return httpx.Timeout(
            timeout=os.getenv("HTTP_TIMEOUT", 30),
            connect=os.getenv("HTTP_CONNECT_TIMEOUT", 45),
        )

    def download_html(self) -> str:
        """Responsible for download HTML from URL

        Raises:
            AttributeError: If the URL is invalid or the HTML cannot be downloaded.

        Returns:
            str: The downloaded HTML content.
        """
        try:

            response = self.client().get(
                self.url,
                timeout=30,
                headers={
                    "User-Agent": "SangueJa/1.0 (+https://whatsapp.com/channel/0029VbDs7Jv47XeJnANDSG3l)"
                },
            )

            response.raise_for_status()

            return response
        except httpx.HTTPError as error:
            raise RuntimeError(f"failed to download #{error}") from error

    def send(self, params: dict = None, headers: dict = None) -> str:
        """Send a POST request to the configured URL.

        Args:
            headers: HTTP headers to include in the request.
            params: Query parameters to include in the request.

        Returns:
            The HTTP response returned by the server.

        Raises:
            RuntimeError: If the request fails or returns an HTTP error.
        """
        try:

            response = self.client().post(
                self.url,
                timeout=30,
                headers=headers,
                params=params,
            )

            response.raise_for_status()

            return response
        except httpx.HTTPError as error:
            raise RuntimeError(f"failed to download #{error}") from error
