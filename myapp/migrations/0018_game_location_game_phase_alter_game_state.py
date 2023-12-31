# Generated by Django 4.2.3 on 2023-08-11 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_remove_location_competition'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.location'),
        ),
        migrations.AddField(
            model_name='game',
            name='phase',
            field=models.CharField(choices=[('GROUP', 'Group'), ('ROUND_OF_16', '16th Round'), ('QUARTER_FINALS', 'Quarter Finals'), ('SEMI_FINALS', 'Semi Finals'), ('FINAL', 'Final')], default='Group', max_length=50),
        ),
        migrations.AlterField(
            model_name='game',
            name='state',
            field=models.CharField(choices=[('FINALLY', 'Finally'), ('NOT_PLAYED', 'Not played'), ('SUSPENDED', 'Suspended'), ('CANCELLED', 'Cancelled'), ('POSTPONED', 'Postponed')], default='Not played', max_length=50),
        ),
    ]
