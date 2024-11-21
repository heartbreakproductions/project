# chat/templatetags/highlight.py
from django import template
import re

register = template.Library()

@register.filter
def highlight_usernames(value):
    return re.sub(r'@(\w+)', r'<span class="text-red-500">@\1</span>', value)
