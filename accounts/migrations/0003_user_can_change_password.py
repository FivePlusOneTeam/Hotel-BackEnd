# Generated by Django 4.2.7 on 2023-11-22 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_employee_id_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_change_password',
            field=models.BooleanField(default=False),
        ),
    ]
