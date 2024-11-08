# blog/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.apps import apps
from .models import Blog

@receiver(post_save, sender=Blog)
def notify_users_on_new_blog(sender, instance, created, **kwargs):
    if created:  # Only send notifications for newly created blog posts
        Notification = apps.get_model('notifications', 'Notification')  # Dynamically get the Notification model
        users = User.objects.all()

        for user in users:
            Notification.objects.create(
                recipient=user,
                notification_type='new_blog',
                blog=instance
            )
