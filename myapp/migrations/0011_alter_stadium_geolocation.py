# Generated by Django 4.2.3 on 2023-08-07 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_stadium'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stadium',
            name='geolocation',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
