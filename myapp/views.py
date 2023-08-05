from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required

from .forms import PlayerForm, SportForm, CompetitionForm, CustomPlayerForm, TeamForm
from .models import Competition, Season, Sport, Group, Team, Player, Game, State, PlayerTeamSeason, Inscription
from .utils import generate_groups_for_season


def inscription_team(request, id_competition, id_team):
    team = get_object_or_404(Team, pk=id_team)
    competition = get_object_or_404(Competition, pk=id_competition)

    if request.method == 'POST':
        form = CustomPlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            player.save()
            return redirect('competition_detail', id_competition=id_competition)

    else:
        form = CustomPlayerForm()

    return render(request, 'inscription_team.html', {
        'form': form,
        'team': team,
    })


@login_required  # Asegúrate de que el usuario esté autenticado para crear un equipo
def new_team(request, id):
    competition = get_object_or_404(Competition, pk=id)

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.user = request.user  # Asignar el usuario al equipo
            team.competition = competition  # Asignar la competencia al equipo
            team.save()
            return redirect('competition_detail', id=id)
    else:
        form = TeamForm()

    return render(request, 'new_team.html', {
        'form': form,
        'competition': competition,
    })


@login_required
@transaction.atomic
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


@login_required
def standings_table(request):
    teams = Team.objects.all()
    standings = {team: team.get_standings() for team in teams}

    sorted_standings = sorted(standings.items(), key=lambda x: (x[1]['points'], x[1]['goals_difference']), reverse=True)

    return render(request, 'standings_table.html', {
        'standings': sorted_standings,
    })


@login_required
def game_detail(request, id):
    game = get_object_or_404(Game, pk=id)
    return render(request, 'game_detail.html', {'game': game})


@login_required
def game_list(request):
    games = Game.objects.all()
    states = State.choices
    sports = Sport.objects.all()
    selected_state = request.GET.get('state')

    if selected_state and selected_state in dict(State.choices):
        games = games.filter(state=selected_state)

    selected_sport = request.GET.get('sport')

    if selected_sport:
        games = games.filter(
            Q(team_local__inscription__sport_list_id=selected_sport) |
            Q(team_visitor__inscription__sport_list_id=selected_sport)
        )

    return render(request, 'game_list.html', {
        'games': games,
        'states': states,
        'sports': sports,
        'selected_state': selected_state,
        'selected_sport': selected_sport,
    })


@login_required
def player_list(request):
    players = Player.objects.all()
    return render(request, 'players.html', {'players': players})


@login_required
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


@login_required
def teams_detail(request, id):
    team = get_object_or_404(Team, pk=id)

    player_team_seasons = PlayerTeamSeason.objects.filter(team=team)

    players = [player_team_season.player for player_team_season in player_team_seasons]

    games_as_local = Game.objects.filter(team_local=team)
    games_as_visitor = Game.objects.filter(team_visitor=team)

    return render(request, 'team_detail.html', {
        'team': team,
        'players': players,
        'games_as_local': games_as_local,
        'games_as_visitor': games_as_visitor,
    })


@login_required
def new_player(request):
    if request.method == 'POST':
        form = CustomPlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_list')
    else:
        form = CustomPlayerForm()

    return render(request, 'new_player.html', {'form': form})


@login_required
def competition_list(request):
    competitions = Competition.objects.filter(user=request.user)
    return render(request, 'competitions.html', {'competitions': competitions})


@login_required
def team_list(request):
    teams = Team.objects.filter(user=request.user)
    return render(request, 'teams.html', {'teams': teams})


@login_required
def competition_detail(request, id):
    competition = get_object_or_404(Competition, pk=id)
    seasons = Season.objects.filter(competition=competition)
    teams = Team.objects.all()
    return render(request, 'competition_detail.html', {
        'competition': competition,
        'teams': teams,
        'seasons': seasons,
    })


def home(request):
    if request.user.is_authenticated:
        active_competitions = Competition.objects.filter(is_active=True, user=request.user)
        upcoming_competitions = Competition.objects.filter(is_active=False, user=request.user)

        sports_offered = Sport.objects.all()
        return render(request, 'home.html', {
            'active_competitions': active_competitions,
            'upcoming_competitions': upcoming_competitions,
            'sports_offered': sports_offered,
        })
    else:
        return render(request, 'home.html')


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


@login_required
def new_sport(request):
    if request.method == 'GET':
        form = SportForm()
        return render(request, 'new_sport.html', {'form': form})
    else:
        try:
            form = SportForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            return redirect('new_competition')
        except ValueError:
            return render(request, 'new_sport.html', {
                'form': SportForm,
                'error': 'Bad data passed in. Try again.'
            })


@login_required
@transaction.atomic  # Aplicamos el decorador para asegurar el uso de transacciones
def new_competition(request):
    if request.method == 'GET':
        form = CompetitionForm()
        return render(request, 'new_competition.html', {'form': form})
    else:
        try:
            form = CompetitionForm(request.POST, request.FILES)
            if form.is_valid():
                # Asignar el usuario autenticado al campo "user" antes de guardar la competencia
                competition = form.save(commit=False)
                competition.user = request.user
                competition.save()
                return redirect('competitions')
        except ValueError:
            return render(request, 'new_competition.html', {
                'form': form,
                'error': 'Bad data passed in. Try again.'
            })


def default_page(request):
    if request.user.is_authenticated:
        # Si el usuario está autenticado, redirigir a la página de inicio para usuarios autenticados
        return redirect('home')
    else:
        # Si el usuario no está autenticado, redirigir a la página de inicio para usuarios no autenticados
        return redirect('home')


def competition_seasons(request, id):
    competition = get_object_or_404(Competition, pk=id)
    seasons = Season.objects.filter(competition=competition)
    
    return render(request, 'competition_seasons.html', {'competition': competition, 'seasons': seasons})
