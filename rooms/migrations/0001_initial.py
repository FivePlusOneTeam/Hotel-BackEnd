# Generated by Django 4.2.7 on 2023-11-27 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('o', 'معمولی'), ('v', 'vip')], max_length=1)),
                ('bed_count', models.IntegerField()),
                ('features', models.TextField()),
                ('price_one_night', models.IntegerField()),
                ('code', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('has_Resev', models.BooleanField(default=False)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.roomtype')),
            ],
        ),
    ]