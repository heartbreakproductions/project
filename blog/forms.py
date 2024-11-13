# blog/forms.py
from django import forms
from .models import Comment, Blog

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'body', 'image', 'status']