# Generated by Django 2.2 on 2020-05-25 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialMedia', '0007_auto_20200525_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body',
            field=models.TextField(blank=True),
        ),
    ]
