import logging
import os
from typing import List
from twilio.rest import Client


class NotificationService:
    def __init__(self):
        self.client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_AUTH_TOKEN"])
        self.from_phone: str = os.environ["TWILIO_PHONE"]
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_alert(self, message: str, subscribers: List[str]) -> None:
        for phone in subscribers:
            try:
                self.client.messages.create(body=message, from_=self.from_phone, to=phone)
                self.logger.info(f"Sent alert to phone {phone}: {message}")
            except Exception as e:
                self.logger.error(f"Error sending alert to {phone}: {e}")
                raise
