import itertools
import random
from datetime import timedelta

from .models import Game, Location, Phase


def generate_game_schedule(season, teams_per_group, locations):
    group_matches = generate_group_matches(season, teams_per_group)
    assign_dates_and_locations(group_matches, season.date_start, locations)


def generate_group_matches(season, teams_per_group):
    groups = season.groups.all()  # Obtener los grupos de la temporada
    print(groups)
    group_matches = []

    for group in groups:
        teams = list(group.teams.all())
        matches = list(itertools.combinations(teams, 2))
        random.shuffle(matches)

        group_matches.extend(matches)

    return group_matches


def assign_dates_and_locations(group_matches, start_date, locations):
    days_between_matches = 3  # Intervalo entre partidos en días
    current_date = start_date

    for match in group_matches:
        home_team, away_team = match
        location = get_random_location(locations)

        create_game(home_team, away_team, current_date, location)

        current_date += timedelta(days=days_between_matches)


def get_random_location(locations):
    return random.choice(locations)


def create_game(home_team, away_team, game_date, location):
    game = Game.objects.create(
        team_local=home_team,
        team_visitor=away_team,
        date=game_date,
        location=location,
        phase=Phase.GROUP.value
    )
