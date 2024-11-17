from django.db import models
from django.contrib.auth.models import User
import os

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.pk:
            existing = UserProfile.objects.filter(pk=self.pk).first()
            if existing and existing.profile_image and existing.profile_image != self.profile_image:
                old_image_path = existing.profile_image.path
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
        super().save(*args, **kwargs)