# Generated by Django 2.0.5 on 2018-07-30 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0003_auto_20180730_0922'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='floor',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='floor',
            name='number',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
