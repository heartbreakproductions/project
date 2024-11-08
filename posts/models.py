
    
from django.db import models
from django.contrib.auth.models import User
import os
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_authored')
    upvotes = models.PositiveIntegerField(default=0)  # Add upvotes field
    downvotes = models.PositiveIntegerField(default=0)  # Add downvotes field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check if a new image is being uploaded
        if self.pk:
            existing = Post.objects.filter(pk=self.pk).first()
            if existing and existing.image and existing.image != self.image:
                # Delete the old image if it exists
                old_image_path = existing.image.path
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)

        super().save(*args, **kwargs)

    # class Meta:
    #     ordering = ['-created_at']  # Order by creation date, assuming you add created_at field


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_comments')  # Unique related_name
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')  # Unique related_name
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')])

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} - {self.post.title} ({self.vote_type})"
