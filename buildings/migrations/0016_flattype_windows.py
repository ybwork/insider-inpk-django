# Generated by Django 2.0.5 on 2018-10-04 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0015_flat_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='flattype',
            name='windows',
            field=models.TextField(blank=True),
        ),
    ]
