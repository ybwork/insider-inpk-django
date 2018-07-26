# Generated by Django 2.0.5 on 2018-07-26 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(db_index=True, max_length=16)),
                ('company_hash_id', models.CharField(db_index=True, max_length=16)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('is_agree_with_save_personal_data', models.BooleanField()),
                ('api_key', models.CharField(db_index=True, max_length=255)),
                ('is_confirmed_email', models.BooleanField(default=False)),
                ('is_confirmed_phone', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(db_index=True, default=False)),
                ('email_code', models.CharField(max_length=255, null=True)),
                ('phone_code', models.PositiveIntegerField(default=0)),
                ('password_code', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(db_index=True, max_length=16)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Company'),
        ),
    ]
