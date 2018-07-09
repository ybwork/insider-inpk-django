# Generated by Django 2.0.5 on 2018-07-09 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0003_auto_20180706_1243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='confirm_email',
            new_name='is_confirmed_email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='confirm_phone',
            new_name='is_confirmed_phone',
        ),
        migrations.AddField(
            model_name='user',
            name='email_code',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
