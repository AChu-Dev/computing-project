from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32)
    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=32)
    permission = models.IntegerField(default=0)
    num_fav_resorts = models.IntegerField(default=0)

    def __self__(self):
        return self.firstName, self.lastName

    @property
    def path(self):
        return f"/user/{self.pk}/"


class Resort(models.Model):
    name = models.CharField(max_length=48)
    address = models.CharField(max_length=64)
    longitude = models.DecimalField(max_digits=7, decimal_places=5)
    latitude = models.DecimalField(max_digits=7, decimal_places=5)
    description = models.CharField(max_length=256)

    def __self__(self):
        return self.name


class Favourite(models.Model):
    resort_id = models.ForeignKey(Resort, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
