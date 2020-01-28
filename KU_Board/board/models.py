from django.db import models
from datetime import datetime

# Create your models here.

class Post(models.Model):
    boardNum = models.IntegerField(primary_key=True)
    nickname = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    recommend = models.IntegerField(default = 0)
    unrecommend = models.IntegerField(default = 0)
    date = models.DateTimeField('date published')
    category = models.CharField(max_length=10)
    Field = models.IntegerField(default = 0)

    def count_up(self):
        self.Field += 1
        self.save()

    def __str__(self):
        return self.title



