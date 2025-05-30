from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import profile_view, delete_account, profile_edit

# urlpatterns = [
#     path('register/', views.register, name='register'),
#     path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
#     path('profile/', profile_view, name='profile_view'),
#     path('profile/delete/', delete_account, name='delete_account'),
# ]


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('profile/', profile_view, name='profile_view'),
    # path('profile/<str:username>/', profile_view, name='profile_view'),  # Added username parameter
    path('profile/delete/', delete_account, name='delete_account'),
    path('profile/<str:username>/', profile_view, name='profile_view'),
    path('profile/<str:username>/edit/', profile_edit, name='profile_edit'),
]




