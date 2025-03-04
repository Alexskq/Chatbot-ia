"""
ASGI config for chatbot_ia project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_ia.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chatbot.consumers import ChatConsumer

http_application = get_asgi_application()

websocket_urlpatterns = [
    path('ws/chat/<str:simulation_id>/', ChatConsumer.as_asgi()),
    path('ws/chat/test/', ChatConsumer.as_asgi()),  # Route de test
]

application = ProtocolTypeRouter({
    "http": http_application,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
