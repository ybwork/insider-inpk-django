# Generated by Django 2.0.5 on 2018-09-12 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0007_floortype_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='flattype',
            name='number',
            field=models.IntegerField(null=True),
        ),
    ]
