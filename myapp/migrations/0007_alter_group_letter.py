# Generated by Django 4.2.3 on 2023-08-06 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_group_teams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='letter',
            field=models.CharField(max_length=40),
        ),
    ]