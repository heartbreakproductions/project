from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from django.http import JsonResponse
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from accounts.models import UserProfile


def chat_view(request):
    """
    Renders the chat page with all messages. 
    No nested replies are fetched since replies logic has been removed.
    """
    messages = Message.objects.all().order_by('timestamp')  # Fetch all messages in chronological order
    return render(request, 'chat/chat.html', {'messages': messages})


def get_user_profile_image(request, username):
    """
    Returns the profile image URL of a user, or None if the user has no profile image.
    """
    try:
        user_profile = UserProfile.objects.get(user__username=username)
        if user_profile.profile_image:
            return JsonResponse({'profile_image_url': user_profile.profile_image.url})
        else:
            return JsonResponse({'profile_image_url': None})
    except UserProfile.DoesNotExist:
        return JsonResponse({'profile_image_url': None})


def delete_message(request, message_id):
    """
    Deletes a specific message if the current user is its owner.
    Sends a WebSocket notification if deletion is successful.
    """
    if request.method == 'POST':
        message = get_object_or_404(Message, id=message_id)
        if message.user == request.user:
            message.delete()

            # Notify WebSocket group about the deletion
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "chat_global_chat",  # Update this if using a different group naming convention
                {
                    "type": "chat_delete_message",
                    "message_id": message_id,
                },
            )

            return redirect('chat')  # Redirect to the chat page
        else:
            messages.error(request, 'You do not have permission to delete this message.')
            return redirect('chat')

    return redirect('chat')  # Redirect if request is not POST


