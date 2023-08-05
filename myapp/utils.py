# utils.py
from math import ceil
from random import shuffle
from .models import Group, Inscription


def generate_groups_for_season(season, competition_modality='T'):
    inscriptions = Inscription.objects.filter(season=season)  # Obtener las inscripciones para la temporada
    teams = [inscription.team for inscription in inscriptions]  # Obtener los equipos inscritos en la temporada
    num_teams = len(teams)

    if competition_modality == 'E':
        # En el caso de una competencia estilo liga, generamos un solo grupo con todos los equipos
        group = Group.objects.create(letter='A', season=season)
        group.teams.set(teams)
    else:
        # En el caso de una competencia estilo torneo, dividimos los equipos en grupos de manera aleatoria
        shuffle(teams)
        num_groups = ceil(
            num_teams / 4)  # Ejemplo: Cada grupo tendrá 4 equipos, pero puede ser ajustado según tus necesidades

        for i in range(num_groups):
            group = Group.objects.create(letter=chr(65 + i), season=season)
            group_teams = teams[i * 4: (i + 1) * 4]
            group.teams.set(group_teams)

            # Si los equipos están inscritos mediante una tabla de inscripción (Inscription),
            # podemos crear las relaciones entre el grupo y los equipos inscritos.
            # Asumiendo que la relación entre Group e Inscription es ForeignKey a Group,
            # y la relación entre Inscription y Team es ForeignKey a Team.
            for team in group_teams:
                Inscription.objects.create(group=group, team=team)

        # Si quedan equipos sin asignar a un grupo, podemos crear un grupo adicional con esos equipos
        remaining_teams = teams[num_groups * 4:]
        if remaining_teams:
            group = Group.objects.create(letter=chr(65 + num_groups), season=season)
            group.teams.set(remaining_teams)

            # Crear las relaciones para los equipos inscritos en el grupo adicional
            for team in remaining_teams:
                Inscription.objects.create(group=group, team=team)
