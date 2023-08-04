# Generated by Django 4.2.3 on 2023-08-04 05:02

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
                ('name', models.CharField(blank=True, max_length=50)),
                ('date_start', models.DateField(null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('sport', models.CharField(choices=[('F', 'Football'), ('B', 'Basketball'), ('V', 'Volleyball'), ('H', 'Handball'), ('T', 'Tennis'), ('O', 'Other')], default='F', max_length=1)),
                ('genre', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('MF', 'Mixed')], max_length=2, null=True)),
                ('number_grups', models.IntegerField(blank=True, null=True)),
                ('type_competition', models.CharField(choices=[('L', 'League'), ('T', 'Tournament'), ('P', 'Playoff'), ('F', 'Friendly'), ('GS', 'Group Stage'), ('O', 'Other')], default='O', max_length=2)),
                ('is_active', models.BooleanField(default=True)),
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
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter', models.CharField(max_length=1)),
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
                ('image', models.ImageField(blank=True, null=True, upload_to='sport_images/')),
                ('type_sport', models.CharField(blank=True, choices=[('I', 'Individual'), ('T', 'Team')], default='T', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('competition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='myapp.competition')),
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
            name='PlayerTeamSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.player')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.season')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.team')),
            ],
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.group')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.team')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='myapp.season'),
        ),
        migrations.AddField(
            model_name='game',
            name='loser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='losing_games', to='myapp.team'),
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
            model_name='game',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winning_games', to='myapp.team'),
        ),
    ]
