# Generated by Django 4.0.5 on 2022-06-06 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0011_alter_employee_job_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='is_admin',
        ),
    ]