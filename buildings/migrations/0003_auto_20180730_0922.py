# Generated by Django 2.0.5 on 2018-07-30 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0002_auto_20180727_1742'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='floortype',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='floortype',
            name='number_of_flats',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
