import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # Import your routing after Django is set up

# Set the default settings module for the Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Initialize Django application to make sure apps are ready
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
