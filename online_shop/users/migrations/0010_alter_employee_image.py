# Generated by Django 4.1.3 on 2023-01-30 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_employee_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='image',
            field=models.ImageField(default=None, upload_to='images/employees'),
        ),
    ]
