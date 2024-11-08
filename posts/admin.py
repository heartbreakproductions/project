from django.contrib import admin
from .models import Post, Comment, Favorite

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'image')
    search_fields = ('title', 'body')
    list_filter = ('author',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'is_reply')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at',)

    def is_reply(self, obj):
        return obj.parent is not None  # Check if the comment has a parent
    is_reply.boolean = True  # Display as a boolean icon in the admin

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    search_fields = ('user__username', 'post__title')
