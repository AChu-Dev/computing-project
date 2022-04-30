from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

class User(models.Model):
#    id = models.ForeignKey(User, primary_key=True, default=1, on_delete=models.CASCADE, unique=True)
    username = models.CharField(max_length=32)
    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(max_length=64)
    permission = models.IntegerField()
    num_fav_resorts = models.IntegerField()

    def __self__(self):
        return self.firstName, self.lastName


class Resort(models.Model):
    name = models.CharField(max_length=48)
    address = models.CharField(max_length=64)
    longitude = models.DecimalField(max_digits=7, decimal_places=5)
    latitude = models.DecimalField(max_digits=7, decimal_places=5)

    def __self__(self):
        return self.name
