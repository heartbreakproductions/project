# groups/admin.py
from django.contrib import admin
from .models import Group, Membership, Post, Comment

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'joined_at')
    search_fields = ('user__username', 'group__name')
    list_filter = ('joined_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'group', 'created_at')
    search_fields = ('title', 'author__username', 'group__name')
    list_filter = ('created_at', 'group')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'parent')
    search_fields = ('user__username', 'post__title', 'content')
    list_filter = ('created_at',)
