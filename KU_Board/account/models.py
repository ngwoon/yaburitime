from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

<<<<<<< HEAD:KU_Board/account/models.py

class User(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    pw = models.CharField(max_length=20)
    username = models.CharField(max_length=10)
    nickname = models.CharField(max_length=10)
=======
class CustomUser(AbstractUser):
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nickname
>>>>>>> dev-join:KU_Board/join/models.py
