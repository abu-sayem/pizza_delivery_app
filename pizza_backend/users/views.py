# users/views.py
from rest_framework import generics
from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets, permissions

from .serializers import UserSerializer

from . import models
from . import serializers

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
