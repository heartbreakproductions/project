
from django.contrib import admin
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # path('', views.Homepage.as_view(),name='home'),
    path('donate/', views.donate_page, name='donate_page'),
    path('about/', views.about_page, name='about_page'),
    path('links/', views.links_page, name='links_page'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('posts.urls')),
    path('blog/', include('blog.urls')),
    path('services/', include('services.urls')),
    path('jobs/', include('jobs.urls', namespace='jobs')),
    path('groups/', include('groups.urls', namespace='groups')),
    path('notifications/', include('notifications.urls')),
    path('chat/', include('chat.urls')),
    
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)