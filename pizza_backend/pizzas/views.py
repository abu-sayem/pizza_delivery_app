from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets

from .models import Order, Pizza
from  .serializers import OrderSerializer, PizzaSerializer, OrderSerializerCreateRetrive

class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    def get_queryset(self):
        queryset = Order.objects.all()
        customer_id = self.request.query_params.get('customer_id', None)
        status = self.request.query_params.get('status', None)
        
        if customer_id is not None:
            queryset = queryset.filter(customer__id=customer_id)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = OrderSerializerCreateRetrive(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Order.objects.all()
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializerCreateRetrive(order)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.get("items") if 'items' in request.data else request.data
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        if order.status == "de" and self.request.data['status'] != "de":
            
            response = {
                        "message": "Sorry you Cant change status after delivery"
                    }
            return Response(response, status=status.HTTP_403_FORBIDDEN,)
        else:
            return super().partial_update(request, *args, **kwargs)

