# Generated by Django 2.0.5 on 2018-09-05 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0006_auto_20180905_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='floortype',
            name='number',
            field=models.IntegerField(null=True),
        ),
    ]
