# Generated by Django 4.2.3 on 2023-07-16 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('hour', models.TimeField(default='00:00:00')),
                ('state', models.CharField(choices=[('PLAYED', 'Played'), ('NOT_PLAYED', 'Not played'), ('SUSPENDED', 'Suspended'), ('CANCELLED', 'Cancelled'), ('POSTPONED', 'Postponed')], default='Not played', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Modality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type_modality', models.CharField(choices=[('L', 'League'), ('T', 'Tournament'), ('P', 'Playoff'), ('F', 'Friendly'), ('GS', 'Group Stage'), ('O', 'Other')], default='O', help_text='Type of modality', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('number_player', models.IntegerField()),
                ('position', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type_sport', models.CharField(blank=True, choices=[('I', 'Individual'), ('T', 'Team')], default='I', help_text='Type of sport', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('competition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.competition')),
                ('modality', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.modality')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=50)),
                ('game', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.game')),
            ],
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_list', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.player')),
                ('team_list', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.team')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter', models.CharField(max_length=1)),
                ('inscription_list', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.inscription')),
                ('season', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.season')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='team_local',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teamLocal', to='myapp.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='team_visitor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teamVisitor', to='myapp.team'),
        ),
        migrations.AddField(
            model_name='competition',
            name='sport_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.sport'),
        ),
    ]
