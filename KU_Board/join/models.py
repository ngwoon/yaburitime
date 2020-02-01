from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nickname