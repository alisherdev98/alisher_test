# Generated by Django 4.0.5 on 2022-06-05 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_employee_is_leader'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='is_leader',
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]
