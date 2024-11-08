# blog/urls.py
from django.urls import path
from .views import blog_list, blog_detail, add_comment, delete_comment

app_name = 'blog'

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:slug>/', blog_detail, name='blog_detail'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:slug>/comment/', add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
]
