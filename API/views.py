from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse
from rest_framework import viewsets, generics, authentication, permissions
from .seralizer import UserSerializer, ResortSerializer, FavouriteSerializer
from .models import User, Resort, Favourite
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
# Create your views here.


# USER VIEWS

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all().order_by('firstName')
    serializer_class = UserSerializer
    authentication_classes = [
            authentication.SessionAuthentication,
            ]
    permission_classes = [permissions.AllowAny]

    #def create(self, seralizer):
    #    firstName = seralizer.get('firstName')
    #    lastName = seralizer.get('lastName')
    #    email = seralizer.get('email')
    #    username = seralizer.get('username')

        # firstName = seralizer.validated_data.get('firstName')
        # lastName = seralizer.validated_data.get('lastName')
        # email = seralizer.validated_data.get('email')
        # username = seralizer.validated_data.get('username')
    #    seralizer.save()


user_create_view = UserCreateView.as_view()


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


user_detail_view = UserDetailView.as_view()


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


user_list_view = UserListView.as_view()


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()


user_update_view = UserUpdateView.as_view()


class UserUpdateMixin(SingleObjectMixin, View):
    def dispatch(self, request, pk, *args, **kwargs):
        if request.user.is_staff:
            self.fields = [
                    "username",
                    "firstName",
                    "lastName",
                    "email",
                    "permission",
                    "num_fav_resorts",
                    ]
        else:
            self.fields = [
                    "firstName",
                    "lastName",
                    "email",
                    ]

        return super().dispatch(request, pk, *args, **kwargs)


user_update_mixin = UserUpdateMixin.as_view()


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

    def delete_view(self, serializer):
        instance = serializer.delete()


user_delete_view = UserDeleteView.as_view()


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

# RESORT VIEWS


class ResortViewSet(viewsets.ModelViewSet):
    queryset = Resort.objects.all().order_by('name')
    serializer_class = ResortSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ResortCreateView(APIView):
    def get_object(self, pk):
        try:
            return Resort.objects.get(pk=pk)
        except Resort.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        resorts = Resort.objects.all()
        serializer = ResortSerializer(resorts, many=True)
        return Response(serializer.data)

    def post(self, req, format=None):
        serializer = ResortSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, pk, format=None):
        resort = self.get_object(pk)
        resort.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, req, pk, format=None):
        resort = req.get_object(pk)
        serializer = ResortSerializer(resort, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


resort_api_view = ResortCreateView.as_view()


class ResortCreateViewOld(generics.CreateAPIView):
    queryset = Resort.objects.all().order_by('name')
    serializer_class = ResortSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#    def create(self, seralizer):
 #       name = seralizer.get('name')
  #      address = seralizer.get('address')
   #     longitude = seralizer.get('longitude')
    #    latitude = seralizer.get('latitude')
     #   seralizer.save()


resort_create_view = ResortCreateViewOld.as_view()


class ResortDetailView(generics.RetrieveAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


resort_detail_view = ResortDetailView.as_view()


class ResortListView(generics.ListAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


resort_list_view = ResortListView.as_view()


class ResortDeleteView(generics.DestroyAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

    def delete_view(self, serializer):
        instance = serializer.save()


resort_delete_view = ResortDeleteView.as_view()


class ResortUpdateView(generics.UpdateAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()


resort_update_view = ResortUpdateView.as_view()


class ResortAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

# Favourite


class FavouriteCreateView(generics.CreateAPIView):
    queryset = Favourite.objects.all().order_by('user_id')
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


favourite_create_view = FavouriteCreateView.as_view()


class FavouriteDetailView(generics.RetrieveAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


favourite_detail_view = FavouriteDetailView.as_view()


class FavouriteListView(generics.ListAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


favourite_list_view = FavouriteListView.as_view()


class FavouriteListByUser(generics.ListAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Favourite.objects.all()
            user_id = self.request.GET.get("user_id", None)
            if user_id is not None:
                queryset = queryset.filter(user_id=user_id)
            return queryset


favourite_list_user = FavouriteListByUser.as_view()


class FavouriteListByResort(generics.ListAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Favourite.objects.all()
            resort_id = self.request.GET.get("resort_id", None)
            if resort_id is not None:
                queryset = queryset.filter(resort_id=resort_id)
            return queryset


favourite_list_resort = FavouriteListByResort.as_view()


class FavouriteDeleteView(generics.DestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

    def delete_view(self, serializer):
        instance = serializer.save()


favourite_delete_view = FavouriteDeleteView.as_view()


class FavouriteUpdateView(generics.UpdateAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()


favourite_update_view = FavouriteUpdateView().as_view()


class FavouriteAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'


@api_view(["POST"])
def signup(request):
    username = request.POST['username']
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']

    if User.objects.filter(username=username):
        messages.error(request, "Username already exist! Please try some other username.")
        return HttpResponse("userExists")

    elif User.objects.filter(email=email).exists():
        messages.error(request, "Email Already Registered!!")
        return HttpResponse("emailExists")

    elif password1 != password2:
        messages.error(request, "Passwords didn't matched!!")
        return HttpResponse("passwordNotTheSame")

    newUser = User.objects.create_user(username, email, password1)
    newUser.first_name = firstName
    newUser.last_name = lastName
    newUser.is_active = False
    newUser.save()
    return HttpResponse("success")


@api_view(["POST"])
def signin(request):
    username = request.POST["username"]
    password = request.POST["password"]

    auth = authenticate(username=username, password = password)

    if auth is not None:
        login(request, auth)
        firstName = auth.first_name
        return HttpResponse("success")
    else:
        return HttpResponse("fail")


@api_view(["POST"])
def signout(request):
    logout(request)
    return("success")
