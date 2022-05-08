from django.shortcuts import render
import json
from django.http import JsonResponse
from rest_framework import viewsets, generics, authentication, permissions
from .seralizer import UserSerializer, ResortSerializer, FavouriteSerializer
from .models import User, Resort, Favourite
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
# Create your views here.


# USER VIEWS

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all().order_by('firstName')
    serializer_class = UserSerializer
    authentication_classes = [
            authentication.SessionAuthentication,
#            TokenAuthentication,
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
        instance = serializer.save()


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


class ResortCreateView(generics.CreateAPIView):
    queryset = Resort.objects.all().order_by('name')
    serializer_class = ResortSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#    def create(self, seralizer):
 #       name = seralizer.get('name')
  #      address = seralizer.get('address')
   #     longitude = seralizer.get('longitude')
    #    latitude = seralizer.get('latitude')
     #   seralizer.save()


resort_create_view = ResortCreateView.as_view()


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


class IsAdmin():
    pass


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
