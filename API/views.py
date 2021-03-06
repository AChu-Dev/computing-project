from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, generics, authentication, permissions
from .seralizer import ResortSerializer, FavouriteSerializer, DjangoUserSerializer, DjangoUserSerializerInfo
from .models import Resort, Favourite
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.contrib.auth import models
# Create your views here.

# USER VIEWS Django


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


create_user_django = CreateUserDjango.as_view()


class LoginUserDjango(APIView):
    def get(self):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        pass


class DUserList(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = DjangoUserSerializer


duser_list_view = DUserList.as_view()


class DUserDetail(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = DjangoUserSerializer


duser_detail_view = DUserList.as_view()

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

    def delete(self, request, pk, format=None):
        resort = self.get_object(pk)
        resort.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        resort = self.get_object(pk)
        serializer = ResortSerializer(resort, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


resort_api_id_view = ResortDetailDeleteUpdateView.as_view()


# Favourite
class FavouriteCreateView(APIView):
    def get(self, request, format=None):
        fav = Favourite.objects.all()
        serializer = FavouriteSerializer(fav, many=True)
        return Response(serializer.data)

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

    def delete(self, request, pk, format=None):
        fav = self.get_object(pk)
        fav.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        fav = self.get_object(pk)
        serializer = FavouriteSerializer(fav, data=request.data)
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
