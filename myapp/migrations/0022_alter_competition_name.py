# Generated by Django 4.2.3 on 2023-07-25 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_alter_sport_type_sport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
