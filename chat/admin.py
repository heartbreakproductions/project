from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp')  # Fields to display in the admin list view
    search_fields = ('user__username', 'content')  # Make the `user` and `content` fields searchable
    list_filter = ('timestamp',)  # Add a filter option based on the timestamp

# Alternatively, you can also register the model directly:
# admin.site.register(Message, MessageAdmin)
