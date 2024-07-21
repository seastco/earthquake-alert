from .alert_factory import AlertFactory
from .notification_service import NotificationService
from .storage_service import StorageService

class AlertManager:
    def __init__(self, notification_service=None, storage_service=None):
        self.notification_service = notification_service or NotificationService()
        self.storage_service = storage_service or StorageService()

    def process_alerts(self, alert_types):
        alerts_to_send = []

        for alert_type in alert_types:
            alert = AlertFactory.create_alert(alert_type)
            data = alert.fetch_data()
            for item in data:
                if alert.should_alert(item) and not self.storage_service.alert_already_sent(item['id']):
                    message = alert.format_alert(item)
                    alerts_to_send.append((item['id'], message))

        if alerts_to_send:
            subscribers = self.storage_service.get_subscribers()
            for alert_id, message in alerts_to_send:
                self.notification_service.send_alert(message, subscribers)
                self.storage_service.store_sent_alert(alert_id)