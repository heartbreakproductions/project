# notifications/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user, deleted=False).order_by('-timestamp')
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})


@login_required
def read_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)

    # Mark the notification as read
    notification.read = True
    notification.save()

    # Redirect based on notification type
    if notification.notification_type == 'new_blog' and hasattr(notification, 'blog') and notification.blog:
        return redirect(
            'blog:blog_detail',
            year=notification.blog.publish.year,
            month=notification.blog.publish.month,
            day=notification.blog.publish.day,
            slug=notification.blog.slug,
        )
    elif notification.notification_type == 'reply' and notification.post:
        return redirect('posts:post_detail', post_id=notification.post.id)
    
    # Optionally redirect to a default page if notification type is unrecognized
    return redirect('notification_list')  # Redirect back to notification list


@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    
    # Mark the notification as read before deleting
    notification.read = True
    notification.deleted = True  # Mark as deleted
    notification.save()
    
    return redirect('notification_list')
