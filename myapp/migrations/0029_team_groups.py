# Generated by Django 4.2.3 on 2023-08-04 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_remove_group_inscriptions_remove_team_goals_received_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='teams', to='myapp.group'),
        ),
    ]
