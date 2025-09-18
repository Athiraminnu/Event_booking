from django.db import models


# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10)

    def __str__(self):
        return {self.name}
