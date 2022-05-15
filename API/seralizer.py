from rest_framework import serializers
from .models import User, Resort, Favourite
from django.contrib.auth import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
                "pk",
                "username",
                "firstName",
                "lastName",
                "email",
                "permission",
                "password",
                )


class DjangoUserSerializerInfo(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "is_superuser", "last_login"]


class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "first_name", "last_name", "email",
                "password"]


class ResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resort
        fields = (
                "pk",
                "name",
                "longitude",
                "latitude",
                "description",
                "image",
                )


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = (
                "pk",
                "resort_id",
                "user_id",
                )
