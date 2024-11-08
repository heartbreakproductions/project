# notifications/context_processors.py
from django.contrib.auth.models import User

def unread_notifications_count(request):
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(read=False).count()
    else:
        unread_count = 0
    return {'unread_notification_count': unread_count}
