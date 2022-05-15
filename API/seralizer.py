from rest_framework import serializers
from .models import User, Resort, Favourite
from django.contrib.auth import models, get_user_model


UserModel = get_user_model()

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
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
                username = validated_data["username"],
                password = validated_data["password"],
                )
        return user

    class Meta:
        model = UserModel
        fields = (
                "id",
                "username",
                "password",
                )


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
