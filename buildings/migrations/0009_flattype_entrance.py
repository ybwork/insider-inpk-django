# Generated by Django 2.0.5 on 2018-09-13 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0008_flattype_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='flattype',
            name='entrance',
            field=models.IntegerField(null=True),
        ),
    ]