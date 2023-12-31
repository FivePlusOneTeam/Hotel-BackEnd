# Generated by Django 4.2.7 on 2023-11-08 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nationalCode', models.CharField(max_length=10, unique=True)),
                ('firstName', models.CharField(blank=True, max_length=100, null=True)),
                ('lastName', models.CharField(blank=True, max_length=100, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('code', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
