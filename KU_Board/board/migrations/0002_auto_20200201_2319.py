# Generated by Django 3.0.2 on 2020-02-01 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='recommendCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='unrecommendCount',
            field=models.IntegerField(default=0),
        ),
    ]