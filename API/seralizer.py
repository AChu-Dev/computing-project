from rest_framework import serializers
from .models import User, Resort, Favourite


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
                "num_fav_resorts",
                "password",
                )


class ResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resort
        fields = (
                "pk",
                "name",
                "address",
                "longitude",
                "latitude",
                "description",
                )


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = (
                "pk",
                "resort_id",
                "user_id",
                )
