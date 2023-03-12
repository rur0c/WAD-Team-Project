# Generated by Django 2.2.28 on 2023-03-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotiview', '0009_track_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='track',
            old_name='url',
            new_name='cover_imageURL',
        ),
        migrations.RemoveField(
            model_name='track',
            name='cover_image',
        ),
        migrations.AddField(
            model_name='track',
            name='previewURL',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='track',
            name='trackURL',
            field=models.URLField(blank=True),
        ),
    ]
