# Generated by Django 2.2 on 2020-05-26 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialMedia', '0010_auto_20200526_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='disliker', to='socialMedia.Profile'),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likers', to='socialMedia.Profile'),
        ),
    ]
