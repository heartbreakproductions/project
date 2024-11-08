from .views import post_create, post_list, post_detail, post_update, post_delete, vote_post
from django.urls import path
from . import views

app_name='posts'

urlpatterns = [
    # post
    path('', post_list, name='post_list'),
    path('create/', post_create, name='post_create'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', post_update, name='post_update'),
    path('post/<int:post_id>/delete/', post_delete, name='post_delete'),
    # comment
    
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    
    # URL pattern for replies to specific comments
    path('post/<int:post_id>/comment/<int:parent_id>/', views.add_comment, name='add_comment_reply'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    # search
    path('search/', views.post_search, name='post_search'),  # Add this line for search
    # save post
    path('post/<int:post_id>/favorite/', views.add_to_favorites, name='add_to_favorites'),
    path('post/<int:post_id>/unfavorite/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.favorite_list, name='favorite_list'),  # View for showing favorite posts
    # vote
    path('posts/<int:post_id>/vote/', vote_post, name='vote_post'),
    
]
