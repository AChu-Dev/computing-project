from django.db import models

# Create your models here.

class User(models.Model):
    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    favouriteResorts = models.IntegerField()

    def __self__(self):
        return self.firstName, self.lastName
