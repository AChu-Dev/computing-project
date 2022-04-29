from django.shortcuts import render
from rest_framework import viewsets
from .seralizer import UserSerializer
from .models import User
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('firstName')
    serializer_class = UserSerializer
