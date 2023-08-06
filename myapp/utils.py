import random

from myapp.models import Team


def sort_teams_in_groups(season):
    # Get all the teams registered in the competition
    teams = Team.objects.filter(competencias=season.competencia)

    # Get the number of groups defined in the season
    num_groups = season.number_groups

    # Shuffle the teams randomly
    random.shuffle(teams)

    # Calculate the number of teams per group
    teams_per_group = len(teams) // num_groups

    # Assign teams to the groups
    groups = season.grupos.all()
    team_index = 0

    for group in groups:
        # Assign teams to this group
        for _ in range(teams_per_group):
            team = teams[team_index]
            group.equipos.add(team)
            team_index += 1
