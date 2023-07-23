from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .forms import PlayerForm, SportForm, CompetitionForm
from .models import Competition, Season, Sport, Group, Team, Inscription, Player, Game, State, PlayerTeamSeason


def new_competition(request):
    if request.method == 'GET':
        form = CompetitionForm()
        return render(request, 'new_competition.html', {'form': form})
    else:
        try:
            form = CompetitionForm(request.POST)
            new_competition = form.save(commit=False)
            new_competition.save()
            return redirect('home')
        except ValueError:
            return render(request, 'new_competition.html', {
                'form': CompetitionForm,
                'error': 'Bad data passed in. Try again.'
            })


def edit_player(request, id):
    player = get_object_or_404(Player, pk=id)

    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('player_detail', id=id)
    else:
        form = PlayerForm(instance=player)

    return render(request, 'edit_player.html', {
        'form': form,
        'player': player,
    })


def inscription_details(request, id):
    # Obtener la inscripción específica según el ID
    inscription = get_object_or_404(Inscription, pk=id)

    # Pasar los datos a la plantilla y renderizarla
    return render(request, 'inscription_details.html', {
        'inscription': inscription,
    })


def inscription_list(request):
    # Obtener todas las inscripciones
    inscriptions = Inscription.objects.all()

    # Pasar los datos a la plantilla y renderizarla
    return render(request, 'inscription_list.html', {
        'inscriptions': inscriptions,
    })


def standings_table(request):
    teams = Team.objects.all()
    played_games = Game.objects.filter(state=State.PLAYED)

    for game in played_games:
        game.update_goals()

    standings = {}

    for team in teams:
        wins = played_games.filter(winner=team).count()
        losses = played_games.filter(loser=team).count()
        points = (wins * 3)
        goals_difference = team.goals_scored - team.goals_received

        standings[team] = {
            'wins': wins,
            'losses': losses,
            'points': points,
            'goals_difference': goals_difference,
        }

    sorted_standings = sorted(standings.items(), key=lambda x: (x[1]['points'], x[1]['goals_difference']), reverse=True)

    return render(request, 'standings_table.html', {
        'standings': sorted_standings,
    })


def game_detail(request, id):
    game = get_object_or_404(Game, pk=id)
    return render(request, 'game_detail.html', {'game': game})


def game_list(request):
    games = Game.objects.all()
    states = State.choices
    sports = Sport.objects.all()
    selected_state = request.GET.get('state')

    if selected_state and selected_state in dict(State.choices):
        games = games.filter(state=selected_state)

    selected_sport = request.GET.get('sport')

    if selected_sport:
        games = games.filter(team_local__inscription__sport_list_id=selected_sport) | \
                games.filter(team_visitor__inscription__sport_list_id=selected_sport)

    return render(request, 'game_list.html', {
        'games': games,
        'states': states,
        'sports': sports,
        'selected_state': selected_state,
        'selected_sport': selected_sport,
    })


def player_list(request):
    players = Player.objects.all()
    return render(request, 'players.html', {'players': players})


def player_detail(request, id):
    player = get_object_or_404(Player, pk=id)

    # Obtener todas las relaciones PlayerTeamSeason del jugador
    player_teams_seasons = PlayerTeamSeason.objects.filter(player=player)

    # Obtener todos los equipos del jugador en temporadas distintas
    teams = []
    for player_team_season in player_teams_seasons:
        if player_team_season.team not in teams:
            teams.append(player_team_season.team)

    return render(request, 'player_detail.html', {
        'player': player,
        'teams': teams,
    })


def teams_detail(request, id):
    team = get_object_or_404(Team, pk=id)

    # Obtener todas las relaciones PlayerTeamSeason del equipo en todas las temporadas
    player_team_seasons = PlayerTeamSeason.objects.filter(team=team)

    # Obtener todos los jugadores del equipo en todas las temporadas
    players = [player_team_season.player for player_team_season in player_team_seasons]

    games_as_local = Game.objects.filter(team_local=team)
    games_as_visitor = Game.objects.filter(team_visitor=team)

    return render(request, 'team_detail.html', {
        'team': team,
        'players': players,
        'games_as_local': games_as_local,
        'games_as_visitor': games_as_visitor,
    })


def team_list(request):
    teams = Team.objects.all()
    return render(request, 'teams.html', {'teams': teams})


def seasons_and_groups(request, id):
    competition = get_object_or_404(Competition, pk=id)
    seasons = Season.objects.filter(competition=competition)
    seasons_and_groups = {}

    for season in seasons:
        groups = Group.objects.filter(season=season)
        inscriptions_by_group = {}

        for group in groups:
            inscriptions = Inscription.objects.filter(group=group)
            teams_by_inscription = {}

            for inscription in inscriptions:
                teams = Team.objects.filter(inscription=inscription)
                teams_by_inscription[inscription] = teams

            inscriptions_by_group[group] = teams_by_inscription

        seasons_and_groups[season] = inscriptions_by_group

    return render(request, 'seasons_and_groups.html', {
        'competition': competition,
        'seasons_and_groups': seasons_and_groups,
    })


def new_player(request):
    form = PlayerForm()
    return render(request, 'new_player.html', {'form': form})


def competition_detail(request, id):
    competition = get_object_or_404(Competition, pk=id)
    seasons = Season.objects.filter(competition=competition)
    groups = Group.objects.filter(season__in=seasons)
    return render(request, 'competition_detail.html', {
        'competition': competition,
        'seasons': seasons,
        'groups': groups,
    })


def home(request):
    active_competitions = Competition.objects.filter(is_active=True)
    upcoming_competitions = Competition.objects.filter(is_active=False)

    sports_offered = Sport.objects.all()
    return render(request, 'home.html', {
        'active_competitions': active_competitions,
        'upcoming_competitions': upcoming_competitions,
        'sports_offered': sports_offered,
    })


# Función para registrar un usuario
def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Passwords did not match'
        })


# Función para cerrar sesión
@login_required
def signout(request):
    logout(request)
    return redirect('home')


# Función para iniciar sesión
def signin(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password incorrect'
            })
        else:
            login(request, user)
            return redirect('home')


def competition_list(request):
    competitions = Competition.objects.all()
    return render(request, 'competitions.html', {'competitions': competitions})


def new_sport(request):
    if request.method == 'GET':
        form = SportForm()
        return render(request, 'new_sport.html', {'form': form})
    else:
        try:
            form = SportForm(request.POST)
            new_sport = form.save(commit=False)
            new_sport.save()
            return redirect('home')
        except ValueError:
            return render(request, 'new_sport.html', {
                'form': SportForm,
                'error': 'Bad data passed in. Try again.'
            })
