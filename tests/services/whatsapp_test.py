from unittest import mock
from app.services.whatsapp import Whatsapp


@mock.patch("app.services.whatsapp.Whatsapp.send_notification")
def test_send_notification(mock_send_notification):
    mock_send_notification.return_value = True

    whats = Whatsapp(url="http://localhost")
    response = whats.send_notification(message="Congratz my friend")

    assert response == True
    mock_send_notification.assert_called_once_with(message="Congratz my friend")
