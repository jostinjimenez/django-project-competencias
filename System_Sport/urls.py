from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.urls import path
from django.urls import include
from myapp import views
from myapp.models import Player

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.default_page, name='default_page'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('competitions/', views.competition_list, name='competitions'),
    path('competitions/<int:id>/', views.competition_detail, name='competition_detail'),
    path('competitions/competitions_detail<int:id_competition>/new_team/', views.new_team, name='new_team'),
    path('new_player/', views.new_player, name='new_player'),
    path('new_sport/', views.new_sport, name='new_sport'),
    path('teams/', views.team_list, name='teams'),
    path('teams/<int:id>/', views.teams_detail, name='teams_detail'),
    path('competitions/<int:id_competition>/inscription_player/<int:id_team>', views.inscription_team,
         name='inscription_team'),

    path('competitions/<int:id_competition>/seasons/', views.competition_seasons,
         name='competition_seasons'),

    path('competitions/<int:id_competition>/seasons/<int:id_season>/new_stadium', login_required(views.new_stadium),
         name='new_stadium'),

    path('competitions/<int:id_competition>/seasons/<int:id_season>/', views.season_teams,
         name='season_teams'),

    path('competitions/<int:id_competition>/seasons/<int:id_season>/sortear_grupos/', views.sortear_grupos,
         name='sortear_grupos'),

    path('competitions/<int:id_competition>/seasons/<int:id_season>/match_season', login_required(views.match_season),
         name='match_season'),

    path('competitions/<int:id_competition>/seasons/<int:id_season>/generate_time', login_required(views.generate_time),
         name='generate_time'),

    path('competitions/<int:id_competition>/seasons/<int:id_season>/generate_time/add_availability/<int:id_location>',
         login_required(views.agregar_disponibilidad), name='add_availability'),
    path('competitions/<int:id_competition>/seasons/<int:id_season>/generate_time/add_availability/delete_availability',
         login_required(views.delete_availability), name='delete_availability'),

    path('players', views.player_list, name='players'),
    path('player/<int:id>/', views.player_detail, name='player_detail'),
    path('games/', views.game_list, name='game_list'),
    path('game/<int:id>/', views.game_detail, name='game_detail'),
    path('standings/', views.standings_table, name='standings_table'),
    path('edit_player/<int:id>/', views.edit_player, name='edit_player'),
    path('new_competition/', views.new_competition, name='new_competition'),

    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
