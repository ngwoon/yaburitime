from django.db import models
from django.conf import settings


# Create your models here.


class Post(models.Model):
    boardNum = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    recommend = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='Post_recomment')
    unrecommend = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='Post_unrecomment')
    date = models.DateTimeField(auto_now_add=True)
    category = models.IntegerField(default=0)  # 1-> 자유게시판, 2->비밀게시판
    Field = models.IntegerField(default=0)  # 조회수

    def count_up(self):  # 조회수 증가방식 바꿀필요 있음
        self.Field += 1
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(max_length=300)
    whatpost = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
