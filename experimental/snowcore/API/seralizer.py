from rest_framework import serializers
from .models import User, Resort

class UserSerializer(serializers.ModelSerializer):
#    user_id = serializers.SeriliazerMethodField(read_only=True)
#    permission = serializers.SeriliazerMethodField(read_only=True)
#    num_fav_resorts = serializers.SeriliazerMethodField(read_only=True)
    class Meta:
        model = User
        fields = (
                "username",
                "firstName",
                "lastName",
                "email",)
#                "permission",
#                "num_fav_resorts",
#                "user_id")


class ResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resort
        fields = (
                "name",
                "address",
                "longitude",
                "latitude",
                )
