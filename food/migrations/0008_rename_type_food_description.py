# Generated by Django 4.2.7 on 2024-01-03 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_alter_foodreservation_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='type',
            new_name='description',
        ),
    ]
