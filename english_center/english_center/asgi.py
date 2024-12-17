import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'english_center.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack   
from my_app import routing


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
           routing.websocket_urlpatterns
        )
    )
})