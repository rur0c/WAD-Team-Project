# Generated by Django 2.2.28 on 2023-03-20 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotiview', '0003_auto_20230320_0754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='active',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='date',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='updated',
        ),
    ]
