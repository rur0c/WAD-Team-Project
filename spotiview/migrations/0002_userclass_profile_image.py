# Generated by Django 2.2.28 on 2023-03-22 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotiview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userclass',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='profile_pictures'),
        ),
    ]
