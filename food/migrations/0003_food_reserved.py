# Generated by Django 4.2.7 on 2023-12-09 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_remove_food_reserve_food_day_roomreservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='reserved',
            field=models.IntegerField(default=0),
        ),
    ]
