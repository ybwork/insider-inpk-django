# Generated by Django 2.0.5 on 2018-09-19 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0011_auto_20180919_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='flatschema',
            name='number_of_rooms',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
