from django.urls import path
from .views import chat_view, delete_message,get_user_profile_image

urlpatterns = [
    path('', chat_view, name='chat'),
    path('chat/delete/<int:message_id>/', delete_message, name='delete_message'),
    path('api/user-profile-image/<str:username>/', get_user_profile_image, name='get_user_profile_image'),
]
