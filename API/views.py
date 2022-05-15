from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, generics, authentication, permissions
from .seralizer import UserSerializer, ResortSerializer, FavouriteSerializer, DjangoUserSerializer, DjangoUserSerializerInfo
from .models import User, Resort, Favourite
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.contrib.auth import models, get_user_model
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


# USER VIEWS Django

class DUserList(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = DjangoUserSerializer


duser_list_view = DUserList.as_view()


class DUserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = DjangoUserSerializer


duser_detail_view = DUserList.as_view()

# USER VIEWS OLD


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all().order_by('firstName')
    serializer_class = UserSerializer
    authentication_classes = [
            authentication.SessionAuthentication,
            ]
    permission_classes = [permissions.AllowAny]


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


class ResortListAndCreateView(APIView):
    def get(self, request, format=None):
        resorts = Resort.objects.all()
        serializer = ResortSerializer(resorts, many=True)
        return Response(serializer.data)

    def post(self, reqest, format=None):
        serializer = ResortSerializer(data=reqest.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


resort_api_view = ResortListAndCreateView.as_view()


class ResortDetailDeleteUpdateView(APIView):

    def get_object(self, pk):
        try:
            return Resort.objects.get(pk=pk)
        except Resort.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        resort = self.get_object(pk)
        serializer = ResortSerializer(resort)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, reqest, pk, format=None):
        resort = self.get_object(pk)
        resort.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, reqest, pk, format=None):
        resort = reqest.get_object(pk)
        serializer = ResortSerializer(resort, data=reqest.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


resort_api_id_view = ResortDetailDeleteUpdateView.as_view()


# Favourite
class FavouriteCreateView(APIView):

    def post(self, request, format=None):
        serializer = FavouriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


favourite_create_view = FavouriteCreateView.as_view()


class FavouriteDetailDeleteUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Favourite.objects.get(pk=pk)
        except Favourite.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        fav = self.get_object(pk)
        serializer = FavouriteSerializer(fav)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, reqest, pk, format=None):
        fav = self.get_object(pk)
        fav.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, reqest, pk, format=None):
        fav = reqest.get_object(pk)
        serializer = FavouriteSerializer(fav, data=reqest.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


favourite_api_id_view = FavouriteDetailDeleteUpdateView.as_view()


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


class FavouriteCreateView(APIView):

    def post(self, request, format=None):
        serializer = FavouriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


favourite_create_view = FavouriteCreateView.as_view()

class CreateUserDjango(APIView):
    def get(self, request, format=None):
        users = models.User.objects.all()
        serializer = DjangoUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DjangoUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#    model = get_user_model()
#    permissions = [permissions.AllowAny]
#    serializer_class = DjangoUserSerializer


create_user_django = CreateUserDjango.as_view()


@api_view(["POST"])
def signup(request):
    username = request.POST['username']
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']

    if User.objects.filter(username=username):
        message = messages.error(request, "Username already exist! Please try some other username.")
        return Response(message, status = status.HTTP_400_BAD_REQUEST)

    elif User.objects.filter(email=email).exists():
        message = messages.error(request, "Email Already Registered!!")
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    elif password1 != password2:
        message = messages.error(request, "Passwords didn't matched!!")
        return Response(message, status = status.HTTP_400_BAD_REQUEST)

    newUser = User.objects.create_user(username, email, password1)
    newUser.first_name = firstName
    newUser.last_name = lastName
    newUser.is_active = False
    newUser.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def signin(request):
    username = request.POST["username"]
    password = request.POST["password"]

    auth = authenticate(username=username, password = password)

    if auth is not None:
        login(request, auth)
        firstName = auth.first_name
        return Response("success", status = status.HTTP_201_CREATED)
    else:
        return HttpResponse("fail", status = status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def signout(request):
    logout(request)
    return("success")
