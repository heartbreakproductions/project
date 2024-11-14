from django.contrib.sitemaps import Sitemap
from .models import Post
from django.urls import reverse

class PostSitemap(Sitemap):
    changefreq = 'daily'  # How frequently the content changes
    priority = 0.8  # The importance of this URL relative to others

    def items(self):
        return Post.objects.all()  # Queryset of all posts

    def lastmod(self, obj):
        return obj.created_at  # Field to indicate the last modification time

    # def location(self, obj):
    #     return reverse('posts:post_detail', args=[obj.id])

    def location(self, obj):
        return f'http://onignou.in/{obj.get_absolute_url()}'