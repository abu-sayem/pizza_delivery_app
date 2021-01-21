from django.urls import path
from rest_framework.routers import DefaultRouter
from .apiviews import  OrderViewSet, PizzaViewSet


router = DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
router.register('pizzas', PizzaViewSet, basename='pizzas')

"""
/order/
/order/pk/
/pizza/
/pizza/pk/
"""

urlpatterns = [
]

urlpatterns += router.urls
