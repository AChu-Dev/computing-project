from rest_framework import serializers
from .models import User, Resort, Favourite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
                "username",
                "firstName",
                "lastName",
                "email",
                "permission",
                "num_fav_resorts",)


class ResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resort
        fields = (
                "name",
                "address",
                "longitude",
                "latitude",
                )


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = (
                "resort_id",
                "user_id",
                )
