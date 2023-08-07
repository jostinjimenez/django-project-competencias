import random

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
import enum

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Sport(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='sport_images/', blank=True, null=True)
    TYPE_SPORT = (
        ('I', 'Individual'),
        ('T', 'Team'),
    )
    type_sport = models.CharField(max_length=1, choices=TYPE_SPORT, blank=True, default='T')

    def __str__(self):
        return self.name


class State(models.TextChoices):
    PLAYED = 'Played'
    NOT_PLAYED = 'Not played'
    SUSPENDED = 'Suspended'
    CANCELLED = 'Cancelled'
    POSTPONED = 'Postponed'


class Competition(models.Model):
    name = models.CharField(max_length=50, blank=True)
    date_start = models.DateField(null=True)
    date_end = models.DateField(blank=True, null=True)
    SPORT_lIST = (
        ('F', 'Football'),
        ('B', 'Basketball'),
        ('V', 'Volleyball'),
        ('H', 'Handball'),
        ('T', 'Tennis'),
        ('O', 'Other')
    )
    sport = models.CharField(max_length=1, choices=SPORT_lIST, default='F')
    genre = models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('MF', 'Mixed')], max_length=2, null=True)
    COMPETITION_TYPES = (
        ('L', 'League'),
        ('T', 'Tournament'),
        ('P', 'Playoff'),
        ('F', 'Friendly'),
        ('GS', 'Group Stage'),
        ('O', 'Other')
    )
    type_competition = models.CharField(max_length=2, choices=COMPETITION_TYPES, default='O')
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='competitions')

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=50)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='seasons', null=True)
    number_grups = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def assign_teams_to_groups(self):
        equipos_inscritos = self.competition.teams.all()
        grupos = self.groups.all()

        # Shuffle the registered teams randomly
        equipos_mezclados = list(equipos_inscritos)
        random.shuffle(equipos_mezclados)

        # Assign each team to a group in random order
        for i, equipo in enumerate(equipos_mezclados):
            grupo = grupos[i % len(grupos)]
            grupo.teams.add(equipo)


class Team(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='teams')
    competition = models.ManyToManyField(Competition, through='Inscription', related_name='teams')
    groups = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, related_name='teams')

    def __str__(self):
        return self.name


class Inscription(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='inscriptions', null=True)

    def __str__(self):
        return self.team.name + ' - ' + self.competition.name


class Game(models.Model):
    date = models.DateField()
    hour = models.TimeField(default='00:00:00')
    team_local = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='teamLocal')
    team_visitor = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='teamVisitor')
    state = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in State],
                             default=State.NOT_PLAYED.value)
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='winning_games')
    loser = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='losing_games')

    def __str__(self):
        return self.team_local.name + ' vs ' + self.team_visitor.name

    def get_result(self):
        if self.score:
            return self.score.result
        return "Not played"


class Score(models.Model):
    result = models.CharField(max_length=50)
    game = models.OneToOneField(Game, on_delete=models.CASCADE, null=True)


class Player(models.Model):
    name = models.CharField(max_length=50)
    number_player = models.IntegerField()
    position = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PlayerTeamSeason(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.player.name} - {self.team.name} ({self.season.name})"


class Group(models.Model):
    letter = models.CharField(max_length=40)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='groups', null=True)

    def __str__(self):
        return self.letter


class Stadium(models.Model):
    name = models.CharField(max_length=50)
    number_seats = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stadiums')
    addres = models.CharField(max_length=200)
    geolocation = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Función para crear automáticamente los grupos cuando se crea una temporada
@receiver(post_save, sender=Season)
def create_groups_for_season(sender, instance, created, **kwargs):
    if created and instance.number_grups:
        for i in range(instance.number_grups):
            Group.objects.create(letter=f"Grupo {i + 1}", season=instance)
