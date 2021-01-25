from django.urls import path 
from channels.routing import ProtocolTypeRouter, URLRouter
from .middleware import TokenAuthMiddlewareStack 
from pizzas.consumers import PizzaConsumer


application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack( URLRouter([
        path('pizza/', PizzaConsumer),
    ]),
    ),
})
