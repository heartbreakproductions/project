from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('create/', views.create_group, name='create'),
    path('join/<int:group_id>/', views.join_group, name='join'),
    path('leave/<int:group_id>/', views.leave_group, name='leave'),
    path('delete/<int:group_id>/', views.delete_group, name='delete'),
    path('', views.group_list, name='list'),
    
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    # post
    path('group/<int:group_id>/post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/update/', views.update_post, name='update_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),  # URL for adding a new comment
    path('post/<int:post_id>/comment/<int:parent_id>/', views.add_comment, name='add_comment_reply'),  # URL for replying
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    # vote
    path('post/<int:post_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('post/<int:post_id>/downvote/', views.downvote_post, name='downvote_post'),
]
