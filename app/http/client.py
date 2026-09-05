import httpx


class HttpClient:
    """Responsible for connect server with http

    Args:
        url (str, optional): Pass the URL to connect via HTTP protocol. Defaults to None.
    """

    def __init__(self, url: str = None, method="GET"):
        self.url = url
        self.method = method

    def download_html(self) -> str:
        """Responsible for download HTML from URL

        Raises:
            AttributeError: If the URL is invalid or the HTML cannot be downloaded.

        Returns:
            str: The downloaded HTML content.
        """
        try:
            return httpx.get(self.url)
        except httpx.HTTPError as error:
            raise RuntimeError("failed to download #{error}") from error
