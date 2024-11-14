from django.contrib.sitemaps import Sitemap
from .models import Blog

class BlogSitemap(Sitemap):
    changefreq = 'daily'  # How frequently the content changes
    priority = 0.8  # The importance of this URL relative to others

    def items(self):
        return Blog.objects.all()  # Queryset of all posts

    def lastmod(self, obj):
        return obj.created  # Field to indicate the last modification time
