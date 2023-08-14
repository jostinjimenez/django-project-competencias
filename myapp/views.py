from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required

from .forms import PlayerForm, SportForm, CompetitionForm, TeamForm, SeasonForm, LocationForm, \
    AvailabilityForm

from .models import Competition, Season, Sport, Group, Team, Player, Game, State, PlayerTeamSeason, Location, \
    Availability, Inscription, TeamSeasonInscription

from .utils import generate_game_schedule


def toggle_competition(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    competition.is_active = not competition.is_active
    competition.save()

    message = 'La competición ha sido activada' if competition.is_active else 'La competición ha sido desactivada'

    return JsonResponse({'message': message, 'is_active': competition.is_active})


def inscription_team(request, id_competition, id_team):
    team = get_object_or_404(Team, pk=id_team)
    competition = get_object_or_404(Competition, pk=id_competition)
    players = Player.objects.filter(playerteamseason__team=team)  # Filtrar por el equipo en PlayerTeamSeason

    return render(request, 'inscription_team.html', {
        'team': team,
        'competition': competition,
        'players': players,
    })


@login_required
def new_player(request, id_competition, id_team):
    competition = get_object_or_404(Competition, pk=id_competition)
    team = get_object_or_404(Team, pk=id_team)

    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user  # Asigna el usuario actual al jugador
            player.save()

            PlayerTeamSeason.objects.create(player=player, team=team)

            return redirect('inscription_team', id_competition=id_competition, id_team=id_team)

    else:
        form = PlayerForm()

    return render(request, 'new_player.html', {'form': form})


@login_required
def new_team(request, id_competition):
    competition = get_object_or_404(Competition, pk=id_competition)

    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.user = request.user  # Asignar el usuario actual al equipo
            team.save()

            selected_season = form.cleaned_data.get('season')
            if selected_season:
                TeamSeasonInscription.objects.create(team=team, season=selected_season)
            else:
                Inscription.objects.create(team=team, competition=competition)

            return redirect('competition_detail', id=id_competition)
    else:
        form = TeamForm()

    return render(request, 'new_team.html', {
        'form': form,
        'competition': competition,
    })


@login_required
def new_stadium(request, id_competition, id_season):
    competition = get_object_or_404(Competition, pk=id_competition)

    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            geolocation = request.POST.get('geolocation')

            stadium = form.save(commit=False)
            stadium.geolocation = geolocation
            stadium.user = request.user  # Asigna el usuario actual al estadio

            try:
                stadium.save()
                return redirect('generate_time', id_competition=id_competition, id_season=id_season)
            except Exception as e:
                form.add_error(None, f"An error occurred: {e}")
    else:
        form = LocationForm()

    return render(request, 'new_stadium.html', {
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
    players = Player.objects.filter(user=request.user)
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

    return render(request, 'team_detail.html', {
        'team': team,
        'players': players,
    })


@login_required
def competition_list(request):
    competitions = Competition.objects.filter(user=request.user)
    return render(request, 'competitions.html', {'competitions': competitions})


@login_required
def team_list(request):
    teams = Team.objects.filter(user=request.user)
    return render(request, 'teams.html', {'teams': teams})


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


def default_page(request):
    if request.user.is_authenticated:
        # Si el usuario está autenticado, redirigir a la página de inicio para usuarios autenticados
        return redirect('home')
    else:
        # Si el usuario no está autenticado, redirigir a la página de inicio para usuarios no autenticados
        return redirect('home')


def search_teams(request):
    search_query = request.GET.get('q')
    if search_query:
        teams = Team.objects.filter(Q(name__icontains=search_query) | Q(city__icontains=search_query))
        serialized_teams = [{'id': team.id, 'name': team.name} for team in teams]
        return JsonResponse({'teams': serialized_teams})
    return JsonResponse({'teams': []})


@login_required
def competition_detail(request, id):
    competition = get_object_or_404(Competition, pk=id)
    seasons = Season.objects.filter(competition=competition)
    teams = Team.objects.filter(competition=competition, user=request.user)  # Filtrar por el usuario actual
    all_teams = Team.objects.exclude(competition=competition)  # Todos los equipos que no están en la competencia
    teams_in_seasons = Team.objects.filter(teamseasoninscription__season__competition=competition, user=request.user)

    n_total_teams = len(teams) + len(teams_in_seasons)

    return render(request, 'competition_detail.html', {
        'competition': competition,
        'teams': teams,
        'all_teams': all_teams,
        'seasons': seasons,
        'teams_in_seasons': teams_in_seasons,
        'n_total_teams': n_total_teams,
    })


@login_required
def add_team_to_competition(request, competition_id, team_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    team = get_object_or_404(Team, pk=team_id)

    # Verificar si el equipo ya está inscrito en la competencia
    if competition.teams.filter(id=team_id).exists():
        messages.error(request, f"El equipo '{team.name}' ya está inscrito en esta competencia.")
        return redirect('competition_detail', id=competition_id)

    # Crear una nueva inscripción
    inscription = Inscription(team=team, competition=competition)
    inscription.save()

    messages.success(request, f"El equipo '{team.name}' ha sido añadido a la competencia '{competition.name}'.")
    return redirect('competition_detail', id=competition_id)


@login_required
def generate_test_teams(request, competition_id, num_teams):
    try:
        num_teams = int(num_teams)
        competition = Competition.objects.get(id=competition_id)

        generated_teams = []
        for i in range(num_teams):
            team_name = f"Equipo de Prueba {i + 1}"
            new_team = Team.objects.create(name=team_name)

            # Crear una nueva Inscripción para asociar el equipo y la competencia
            Inscription.objects.create(team=new_team, competition=competition)

            generated_teams.append(new_team)

        return JsonResponse({'message': f'Se generaron {num_teams} equipos de prueba.'})

    except ValueError:
        return JsonResponse({'error': 'Número de equipos no válido.'}, status=400)
    except Competition.DoesNotExist:
        return JsonResponse({'error': 'Competencia no encontrada.'}, status=404)


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


def season_teams(request, id_competition, id_season):
    competition = get_object_or_404(Competition, pk=id_competition)
    season = get_object_or_404(Season, pk=id_season)

    teams = Team.objects.filter(competition=competition, user=request.user)
    teams_in_seasons = Team.objects.filter(teamseasoninscription__season__competition=competition, user=request.user,
                                           teamseasoninscription__season=season)
    groups = Group.objects.filter(season=season)

    return render(request, 'season_teams.html', {
        'competition': competition,
        'season': season, 'teams': teams,
        'groups': groups,
        'teams_in_seasons': teams_in_seasons,
    })


def sortear_grupos(request, id_competition, id_season):
    season = Season.objects.get(id=id_season)
    season.assign_teams_to_groups()
    return redirect('competition_seasons', id_competition=id_competition)


def undo_group_assignment(request, id_competition, id_season):
    season = Season.objects.get(id=id_season)
    season.undo_assign_teams_to_groups()  # Llamamos a una nueva función para deshacer la asignación
    return redirect('competition_seasons', id_competition=id_competition)


def competition_seasons(request, id_competition):
    if request.method == 'GET':
        form = SeasonForm()
        competition = get_object_or_404(Competition, pk=id_competition)
        seasons = Season.objects.filter(competition=competition)
        show_group_warning = request.session.pop('show_group_warning', False)

        return render(request, 'competition_seasons.html', {
            'competition': competition,
            'seasons': seasons,
            'form': form,
            'show_group_warning': show_group_warning,
        })
    else:
        try:
            form = SeasonForm(request.POST)
            if form.is_valid():
                season = form.save(commit=False)
                season.competition = get_object_or_404(Competition, pk=id_competition)
                season.save()
                return redirect('competition_seasons', id_competition=id_competition)
        except ValueError:
            return render(request, 'competition_seasons.html', {
                'form': form,
                'error': 'Bad data passed in. Try again.'
            })


def generate_calendar(request, id_competition, id_season):
    competition = Competition.objects.get(pk=id_competition)
    season = Season.objects.get(pk=id_season)

    if season.games.exists():
        messages.warning(request, 'Los enfrentamientos ya se han generado previamente.')
    else:
        locations = Location.objects.all()  # Obtener todas las ubicaciones disponibles
        teams_per_group = season.get_teams_per_group()
        generate_game_schedule(season, teams_per_group, locations)

    return redirect('match_season', id_competition=id_competition, id_season=id_season)


def update_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    if request.method == 'POST':
        team_local_goals = request.POST.get('team_local_goals', 0)
        team_visitor_goals = request.POST.get('team_visitor_goals', 0)
        game_state = request.POST.get('game_state', '')

        game.team_local_goals = team_local_goals
        game.team_visitor_goals = team_visitor_goals
        game.state = game_state
        game.save()

    return redirect('match_season', id_competition=game.season.competition.id, id_season=game.season.id)


@login_required
def delete_season(request, id_competition, id_season):
    season = get_object_or_404(Season, id=id_season)
    season.delete()
    return redirect('competition_seasons', id_competition=id_competition)


def delete_selected_games(request):
    try:
        if request.method == "POST":
            game_ids = request.POST.getlist("game_ids[]")  # Obtener los IDs de los partidos seleccionados
            Game.objects.filter(id__in=game_ids).delete()  # Eliminar los partidos seleccionados
            return JsonResponse({"message": "Partidos eliminados con éxito"})
        return JsonResponse({"message": "Método no permitido"}, status=405)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def match_season(request, id_competition, id_season):
    competition = get_object_or_404(Competition, pk=id_competition)
    season = get_object_or_404(Season, pk=id_season)
    games = Game.objects.filter(season=season)

    groups_with_teams = all(group.teams.exists() for group in season.groups.all())

    if not groups_with_teams:
        request.session['show_group_warning'] = True
        return redirect('competition_seasons', id_competition=id_competition)

    if 'show_group_warning' in request.session:
        del request.session['show_group_warning']

    return render(request, 'match_season.html', {
        'competition': competition,
        'season': season,
        'games': games,
    })


@login_required
def generate_time(request, id_competition, id_season):
    locations = Location.objects.all()
    competition = get_object_or_404(Competition, pk=id_competition)
    season = get_object_or_404(Season, pk=id_season)
    form = AvailabilityForm()

    # Obtén las disponibilidades actualizadas para cada ubicación
    availability_data = {}
    for location in locations:
        availability_data[
            location.id] = location.availabilities.all()  # Usar 'availabilities' en lugar de 'availability_set'

    context = {
        'locations': locations,
        'form': form,
        'competition': competition,
        'season': season,
        'availability_data': availability_data,
    }

    return render(request, 'generate_time.html', context)


def agregar_disponibilidad(request, id_competition, id_season, id_location):
    if request.method == 'POST':
        location = Location.objects.get(pk=id_location)
        days_available = request.POST.getlist('days_available')  # Obtener la lista de días seleccionados

        for day in days_available:
            availability = Availability(
                location=location,
                days_available=day,
                opening_time=request.POST.get('opening_time'),
                closing_time=request.POST.get('closing_time'),
                date=request.POST.get('date'),
            )
            availability.save()

    return redirect('generate_time', id_competition=id_competition, id_season=id_season)


def delete_availability(request, id_competition, id_season):
    Availability.objects.all().delete()

    return redirect('generate_time', id_competition=id_competition, id_season=id_season)
