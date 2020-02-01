from django.db import models
from django.core.validators import MinLengthValidator
# from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    pw = models.CharField(max_length=20)
    username = models.CharField(max_length=10)
    nickname = models.CharField(max_length=10)