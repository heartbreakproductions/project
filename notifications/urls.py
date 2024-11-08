# notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('read/<int:notification_id>/', views.read_notification, name='read_notification'),
    path('<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),  # Ensure the URL is correct
]
