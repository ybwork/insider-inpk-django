# Generated by Django 2.0.5 on 2018-07-10 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0004_auto_20180709_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_code',
            field=models.PositiveIntegerField(default=0),
        ),
    ]