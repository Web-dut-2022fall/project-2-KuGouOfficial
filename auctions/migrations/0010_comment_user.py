# Generated by Django 4.1.3 on 2022-12-19 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_comment_create_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.CharField(default=None, max_length=64),
        ),
    ]