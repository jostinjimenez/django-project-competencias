from django.db import models

# Create your models here.
import enum

from django.db import models


# Create your models here.
class Inscription(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=50)
    number_player = models.IntegerField()
    position = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=50)
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, related_name='teams', null=True)
    player_list = models.ManyToManyField(Player, related_name='teams')

    # Cambiar la relacion de muchos a muchos por una de uno a muchos para poder hacer que un jugador pertenezca a un solo equipo
    def __str__(self):
        players_list = ', '.join([str(player) for player in self.player_list.all()])
        return f"{self.name} ({players_list})"


class Sport(models.Model):
    name = models.CharField(max_length=50)
    TYPE_SPORT = (
        ('I', 'Individual'),
        ('T', 'Team'),
    )
    type_sport = models.CharField(max_length=1, choices=TYPE_SPORT, blank=True, default='I', help_text='Type of sport')

    def __str__(self):
        return self.name


class State(models.TextChoices):
    PLAYED = 'Played'
    NOT_PLAYED = 'Not played'
    SUSPENDED = 'Suspended'
    CANCELLED = 'Cancelled'
    POSTPONED = 'Postponed'


class Game(models.Model):
    date = models.DateField()
    hour = models.TimeField(default='00:00:00')
    team_local = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='teamLocal')
    team_visitor = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='teamVisitor')
    state = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in State],
                             default=State.NOT_PLAYED.value)

    def __str__(self):
        return self.team_local.name + ' vs ' + self.team_visitor.name


class Score(models.Model):
    result = models.CharField(max_length=50)
    game = models.OneToOneField(Game, on_delete=models.CASCADE, null=True)


class Competition(models.Model):
    name = models.CharField(max_length=50)
    sport_list = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Modality(models.Model):
    name = models.CharField(max_length=50)
    MODALITY_TYPES = (
        ('L', 'League'),
        ('T', 'Tournament'),
        ('P', 'Playoff'),
        ('F', 'Friendly'),
        ('GS', 'Group Stage'),
        ('O', 'Other')
    )
    type_modality = models.CharField(max_length=2, choices=MODALITY_TYPES, default='O', help_text='Type of modality')

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=50)
    modality = models.OneToOneField(Modality, on_delete=models.SET_NULL, null=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    letter = models.CharField(max_length=1)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    inscriptions = models.ManyToManyField(Inscription)

    def __str__(self):
        return self.letter
