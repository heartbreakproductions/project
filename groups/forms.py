from django import forms
from .models import Group, Post, Comment

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']  # Include description field


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']