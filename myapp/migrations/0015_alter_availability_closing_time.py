# Generated by Django 4.2.3 on 2023-08-08 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_alter_availability_days_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='closing_time',
            field=models.TimeField(blank=True, default='00:00:00'),
        ),
    ]