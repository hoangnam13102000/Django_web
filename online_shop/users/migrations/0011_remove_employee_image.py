# Generated by Django 4.1.3 on 2023-01-30 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_employee_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='image',
        ),
    ]