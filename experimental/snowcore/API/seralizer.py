from rest_framework import serializers
from .models import User, Resort

class UserSerializer(serializers.ModelSerializer):
#    id = serializers.SerializerMethodField(read_only=True)
#    permission = serializers.SerializerMethodField(read_only=True)
#    num_fav_resorts = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = (
#                'id',
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
