from django.db import models

# Create your models here.
import enum

from django.db import models


# Create your models here.
class Inscription(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=50)
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, related_name='teams', null=True)
    goals_scored = models.IntegerField(default=0)
    goals_received = models.IntegerField(default=0)

    def __str__(self):
        return self.name


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
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='winning_games')
    loser = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='losing_games')

    def __str__(self):
        return self.team_local.name + ' vs ' + self.team_visitor.name

    def get_result(self):
        if self.score:
            return self.score.result
        return "Not played"

    def update_goals(self):
        if self.state == State.PLAYED:
            local_goals, visitor_goals = map(int, self.score.result.split('-'))
            self.team_local.goals_scored += local_goals
            self.team_local.goals_received += visitor_goals
            self.team_visitor.goals_scored += visitor_goals
            self.team_visitor.goals_received += local_goals
            self.team_local.save()
            self.team_visitor.save()


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


class Player(models.Model):
    name = models.CharField(max_length=50)
    number_player = models.IntegerField()
    position = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Group(models.Model):
    letter = models.CharField(max_length=1)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    inscriptions = models.ManyToManyField(Inscription)

    def __str__(self):
        return self.letter


class PlayerTeamSeason(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.player.name} - {self.team.name} ({self.season.name})"
