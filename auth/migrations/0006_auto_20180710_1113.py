# Generated by Django 2.0.5 on 2018-07-10 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0005_user_password_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password_code',
            field=models.CharField(default='', max_length=255),
        ),
    ]