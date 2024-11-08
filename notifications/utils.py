# notifications/utils.py
from .models import Notification

def send_notification(recipient, notification_type, post):
    try:
        notification = Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            post=post
        )
        print(f"Notification sent to {recipient.username}: {notification_type} for post '{post.title}'")
    except Exception as e:
        print(f"Error sending notification: {e}")