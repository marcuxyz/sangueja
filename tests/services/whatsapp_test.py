from unittest import mock
from app.services.whatsapp import Whatsapp


@mock.patch("app.services.whatsapp.Whatsapp.send_notification")
def test_send_notification(mock_send_notification, monkeypatch):
    mock_send_notification.return_value = True
    monkeypatch.setenv("WHATSAPP_URL", "https://test.whatsapp")
    monkeypatch.setenv("WHATSAPP_TOKEN", "9A8897CGS7")
    monkeypatch.setenv("WHATSAPP_NUMBER", "559899999999")

    whatsapp = Whatsapp()
    response = whatsapp.send_notification(message="Congratz my friend")

    assert response == True
    assert whatsapp.WHATSAPP_URL == "https://test.whatsapp"
    assert whatsapp.WHATSAPP_TOKEN == "9A8897CGS7"
    assert whatsapp.WHATSAPP_NUMBER == "559899999999"
    mock_send_notification.assert_called_once_with(message="Congratz my friend")
