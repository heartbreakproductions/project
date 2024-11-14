"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from posts.sitemap import PostSitemap
from groups.sitemap import GroupSitemap
from blog.sitemap import BlogSitemap


sitemaps = {
    'posts': PostSitemap,
    'groups': GroupSitemap,
    'blog': BlogSitemap,
}


urlpatterns = [
    # path('', views.Homepage.as_view(),name='home'),
    path('donate/', views.donate_page, name='donate_page'),
    path('about/', views.about_page, name='about_page'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('posts.urls')),
    path('blog/', include('blog.urls')),
    path('services/', include('services.urls')),
    path('jobs/', include('jobs.urls', namespace='jobs')),
    path('groups/', include('groups.urls', namespace='groups')),
    path('notifications/', include('notifications.urls')),
    
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)