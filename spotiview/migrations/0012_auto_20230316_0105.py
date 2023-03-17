# Generated by Django 2.2.28 on 2023-03-16 01:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotiview', '0011_auto_20230316_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='userDisLikes',
            field=models.ManyToManyField(related_name='user_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='track',
            name='userLikes',
            field=models.ManyToManyField(related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
