from django.db import models
from django.conf import settings


class Timetable(models.Model):

    table_name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    lessons = models.ManyToManyField('Lesson', blank=True, related_name='Timetable_Lessons')
    is_default = models.BooleanField(default=False)


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=20)
    professor = models.CharField(max_length=10)
    credit = models.IntegerField(default=0)
    where = models.CharField(max_length=10)
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
