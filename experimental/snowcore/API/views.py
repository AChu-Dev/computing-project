from django.shortcuts import render
import json
from django.http import JsonResponse
from rest_framework import viewsets, generics
from .seralizer import UserSerializer, ResortSerializer
from .models import User, Resort
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


# USER VIEWS

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('firstName')
    serializer_class = UserSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all().order_by('firstName')
    serializer_class = UserSerializer

    def create(self, seralizer):
        firstName = seralizer.get('firstName')
        lastName = seralizer.get('lastName')
        email = seralizer.get('email')
        username = seralizer.get('username')

        # firstName = seralizer.validated_data.get('firstName')
        # lastName = seralizer.validated_data.get('lastName')
        # email = seralizer.validated_data.get('email')
        # username = seralizer.validated_data.get('username')
        seralizer.save()
user_create_view = UserCreateView.as_view()


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

user_detail_view = UserDetailView.as_view()


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

user_list_view = UserListView.as_view()


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def update(self, serializer):
        instance = serializer.save()

user_update_view = UserUpdateView.as_view()


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def delete(self, instance):
        super.delete(instance)

user_delete_view = UserDeleteView.as_view()
# RESORT VIEWS

class ResortViewSet(viewsets.ModelViewSet):
    queryset = Resort.objects.all().order_by('name')
    serializer_class = ResortSerializer


class ResortCreateView(generics.CreateAPIView):
    queryset = Resort.objects.all().order_by('name')
    serializer_class = ResortSerializer

    def create(self, seralizer):
        name = seralizer.get('name')
        address = seralizer.get('address')
        longitude = seralizer.get('longitude')
        latitude = seralizer.get('latitude')

        seralizer.save()
resort_create_view = ResortCreateView.as_view()


class ResortDetailView(generics.RetrieveAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer

resort_detail_view = ResortDetailView.as_view()

class ResortListView(generics.ListAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer

resort_list_view = ResortListView.as_view()


@api_view(["GET"])
def api_home(request, *args, **kwargs):
    data = {}
    print(request.GET)
    body = request.body
    try:
        data = json.loads(body)
    except:
        pass

    data['params'] = dict(request.GET)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type

    return JsonResponse(data)


@api_view(['POST'])
def api_post(request, *args, **kwargs):
    seralizer = UserSerializer(data=request.data)
    if seralizer.is_valid(raise_exception=True):
        instance = seralizer.save()
        print(instance)
        return Response(seralizer.data)


def add_favourite(request, *args, **kwargs):
    data = {}
    print(request.GET)
    body = request.body
    try:
        data = json.loads(body)
    except:
        pass

    data['params'] = dict(request.GET)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type


def search(request, *args, **kwargs):
    data = {}
    print(request.GET)
    body = request.body
    try:
        data = json.loads(body)
    except:
        pass

    data['params'] = dict(request.GET)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type


def list_users(request, *args, **kwargs):
    data = {}
    print(request.GET)
    body = request.body
    try:
        data = json.loads(body)
    except:
        pass

    data['params'] = dict(request.GET)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type
