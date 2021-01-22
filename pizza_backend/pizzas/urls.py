from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import  OrderViewSet, PizzaViewSet


router = DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
router.register('', PizzaViewSet, basename='pizzas')

"""
/order/
/order/pk/
/pizza/
/pizza/pk/
"""

urlpatterns = [
]

urlpatterns += router.urls
