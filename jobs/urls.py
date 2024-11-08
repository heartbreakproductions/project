# jobs/urls.py
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),  # Job listing page with access check
    path('subscription-info/', views.subscription_info, name='subscription_info'),  # Subscription info page
    path('<int:pk>/', views.job_detail, name='job_detail'),  # Job detail page
]
