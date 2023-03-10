# Generated by Django 4.1.3 on 2022-12-19 06:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_remove_item_base_bid_remove_item_create_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='base_bid',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='item',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期'),
        ),
        migrations.AddField(
            model_name='item',
            name='cur_bid',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(default=None, max_length=65535),
        ),
        migrations.AddField(
            model_name='item',
            name='img',
            field=models.CharField(default='default.png', max_length=1024),
        ),
        migrations.AddField(
            model_name='item',
            name='item_type',
            field=models.CharField(default=None, max_length=64),
        ),
        migrations.AddField(
            model_name='item',
            name='mod_date',
            field=models.DateTimeField(auto_now=True, verbose_name='最后修改日期'),
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.CharField(default=None, max_length=64),
        ),
        migrations.AddField(
            model_name='item',
            name='title',
            field=models.CharField(default=None, max_length=64, unique=True),
        ),
        migrations.AddField(
            model_name='item',
            name='winner',
            field=models.CharField(default=None, max_length=64),
        ),
    ]
