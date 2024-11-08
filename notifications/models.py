# notifications/models.py
# notifications/models.py
from django.db import models
from django.contrib.auth.models import User
from posts.models import Post as PostFromPosts, Comment as CommentFromPosts  # Import posts and comments from the posts app
from blog.models import Blog  # Import the Blog model
from groups.models import Post as PostFromGroups, Comment as CommentFromGroups  # Import posts and comments from the groups app

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('upvote', 'Upvote'),
        ('reply', 'Reply'),
        ('new_blog', 'New Blog Post'),
        ('group_post', 'New Group Post'),
        ('group_comment', 'Group Comment'),
        ('group_comment_reply', 'Group Comment Reply'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(PostFromPosts, on_delete=models.CASCADE, null=True, blank=True)  # For normal posts
    group_post = models.ForeignKey(PostFromGroups, on_delete=models.CASCADE, null=True, blank=True)  # For group posts
    comment = models.ForeignKey(CommentFromPosts, on_delete=models.CASCADE, null=True, blank=True)  # For normal comments
    group_comment = models.ForeignKey(CommentFromGroups, on_delete=models.CASCADE, null=True, blank=True)  # For group comments
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        if self.notification_type == 'upvote':
            return f"{self.post.author.username} - Your post '{self.post.title}' received an upvote."
        elif self.notification_type == 'reply':
            return f"{self.comment.user.username} replied to your comment on '{self.post.title}'."
        elif self.notification_type == 'group_post':
            return f"New post in group: '{self.group_post.group.name}' by {self.group_post.author.username}"
        elif self.notification_type == 'new_blog':
            return f"New blog post: {self.blog.title}"
        elif self.notification_type == 'group_comment':
            return f"{self.group_comment.user.username} commented on your group post '{self.group_post.title}'."
        return "Notification"


# # notifications/models.py
# from django.db import models
# from django.contrib.auth.models import User
# from posts.models import Post, Comment
# from blog.models import Blog
# from groups.models import Post, Comment


# class Notification(models.Model):
#     NOTIFICATION_TYPES = [
#         ('upvote', 'Upvote'),
#         ('reply', 'Reply'),
#         ('new_blog', 'New Blog Post'),  # Type for new blog posts
#         ('group_post', 'New Group Post'),
#         ('group_comment', 'Group Comment'),
#     ]
    
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#     notification_type = models.CharField(max_length=15, choices=NOTIFICATION_TYPES)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
#     blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     read = models.BooleanField(default=False)
#     deleted = models.BooleanField(default=False)

#     # def __str__(self):
#     #     if self.notification_type == 'upvote':
#     #         return f"{self.post.author.username} - Your post '{self.post.title}' received an upvote."
#     #     elif self.notification_type == 'reply':
#     #         return f"{self.comment.user.username} replied to your comment on '{self.post.title}'."
#     #     elif self.notification_type == 'group_post':
#     #         return f"New post in group: '{self.post.group.name}' by {self.post.author.username}"
#     #     elif self.notification_type == 'new_blog':
#     #         return f"New blog post: {self.blog.title}"
#     #     return "Notification"

#     # def __str__(self):
#     #     if self.notification_type == 'upvote':
#     #         return f"{self.post.author.username} - Your post '{self.post.title}' received an upvote."
#     #     elif self.notification_type == 'comment':
#     #         return f"{self.comment.user.username} commented on your post '{self.post.title}'."
#     #     elif self.notification_type == 'reply':
#     #         return f"{self.comment.user.username} replied to your comment on '{self.post.title}'."
#     #     elif self.notification_type == 'new_blog':
#     #         return f"New blog post: {self.blog.title}"
#     #     elif self.notification_type == 'group_post':
#     #         return f"New post in group: {self.post.group.name}"
#     #     return "Notification"


#     # def __str__(self):
#     #     if self.notification_type == 'upvote':
#     #         return f"{self.post.author.username} - Your post '{self.post.title}' received an upvote."
#     #     elif self.notification_type == 'reply':
#     #         return f"{self.comment.user.username} replied to your comment on '{self.post.title}'."
#     #     elif self.notification_type == 'group_post':
#     #         return f"New post in group: '{self.post.group.name}' by {self.post.author.username}"
#     #     elif self.notification_type == 'new_blog':
#     #         return f"New blog post: {self.blog.title}"
#     #     elif self.notification_type == 'group_comment':
#     #         return f"{self.comment.user.username} commented on your group post '{self.post.title}'."
#     #     return "Notification"