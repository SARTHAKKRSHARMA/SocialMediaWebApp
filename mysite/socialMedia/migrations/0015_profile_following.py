# Generated by Django 2.2 on 2020-05-27 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialMedia', '0014_profile_want_to_be_follower'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followings', to='socialMedia.Profile'),
        ),
    ]
