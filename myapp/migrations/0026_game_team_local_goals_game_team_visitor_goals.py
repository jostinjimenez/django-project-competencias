# Generated by Django 4.2.3 on 2023-08-12 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_game_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='team_local_goals',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='team_visitor_goals',
            field=models.IntegerField(default=0),
        ),
    ]
