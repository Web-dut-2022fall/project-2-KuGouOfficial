import django.utils.timezone as timezone

from django.contrib.auth.models import AbstractUser
from django.db import models

"""
python manage.py makemigrations
python manage.py migrate
"""


class User(AbstractUser):
    pass


class Item(models.Model):
    item_id = models.IntegerField(auto_created=True, primary_key=True, unique=True)
    winner = models.CharField(max_length=64, default=None, blank=True, null=True)
    owner = models.CharField(max_length=64, default=None)
    item_type = models.CharField(max_length=64, default=None)
    title = models.CharField(max_length=64, unique=True, default=None)
    description = models.CharField(max_length=65535, default=None)
    base_bid = models.FloatField(default=None)
    cur_bid = models.FloatField(default=None)
    img = models.CharField(max_length=1024, default='default.png')
    create_date = models.DateTimeField('保存日期', default=timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now=True)



class WatchList(models.Model):
    owner = models.CharField(max_length=64, null=False)
    item_id = models.IntegerField(primary_key=True, unique=True, null=False)


class Comment(models.Model):
    item_id = models.IntegerField(unique=False, null=False)
    user = models.CharField(max_length=64, default=None)
    com = models.CharField(max_length=4096)
    create_date = models.DateTimeField('保存日期', default=timezone.now)
