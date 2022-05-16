from rest_framework import serializers
from .models import User, Resort, Favourite
from django.contrib.auth import models, get_user_model


UserModel = get_user_model()


class DjangoDetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "first_name", "last_name", "data_joined", "is_active", "is_staff"]


class DjangoSuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "is_superuser"]


class DjangoUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = (
                "username",
                "password",
                )

    def create(self, validated_data):
        user = UserModel.objects.create_user(
                username = validated_data["username"],
                password = validated_data["password"],
                )
        user.set_password(validated_data["password"])
        user.save()
        return user




class DjangoLogin(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
                "username",
                "email"
                )

class DjangoRegister(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
                "id",
                "username",
                "email",
                "password",
                )
        extra_kwargs = {"password" : {"write_only": True}}

        def create(self, data):
            user = models.User.objects.create_user(data["username"], data["email"], data["password"])
            user.set_password(data["password"])
            user.save()
            return user



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
2

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = (
                "pk",
                "resort_id",
                "user_id",
                )
