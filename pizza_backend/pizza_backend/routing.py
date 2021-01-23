from django.urls import path 
from channels.routing import ProtocolTypeRouter, URLRouter

from pizzas.consumers import PizzaConsumer


application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('pizza/', PizzaConsumer),
    ]),
})
