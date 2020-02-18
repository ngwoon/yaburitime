# Generated by Django 3.0.2 on 2020-02-18 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_name', models.CharField(max_length=20)),
                ('professor', models.CharField(max_length=10)),
                ('credit', models.IntegerField(default=0)),
                ('where', models.CharField(max_length=10)),
                ('starttime', models.TimeField(blank=True, null=True)),
                ('endtime', models.TimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_default', models.BooleanField(default=False)),
                ('lessons', models.ManyToManyField(blank=True, related_name='Timetable_Lessons', to='timetable.Lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]