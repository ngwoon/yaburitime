from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=10, validators=[MinLengthValidator(5, "아이디는 5글자 이상 10자 이하여야 합니다.")], primary_key=True)
    password = models.CharField(max_length=100, validators=[MinLengthValidator(5, "패스워드는 5글자 이상 15자 이하여야 합니다.")])
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(3, "닉네임은 3글자 이상 10자 이하여야 합니다.")])

    def __str__(self):
        return self.nickname
