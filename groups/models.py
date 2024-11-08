from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups')
    created_at = models.DateTimeField(auto_now_add=True)  # Temporarily comment this out
    members = models.ManyToManyField(User, through='Membership', related_name='joined_groups')

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
    
class Vote(models.Model):
    VOTE_TYPE_CHOICES = (
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_votes')  # Unique related_name
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='group_votes')  # Adjust this too
    vote_type = models.CharField(max_length=8, choices=VOTE_TYPE_CHOICES)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} {self.vote_type}d {self.post.title}'