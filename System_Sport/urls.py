from django.contrib import admin
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
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('competitions/', views.competition_list, name='competitions'),
    path('competitions/competitions_detail/<int:id>/', views.competition_detail, name='competition_detail'),
    path('new_player/', views.new_player, name='new_player'),
    path('new_sport/', views.new_sport, name='new_sport'),
    path('competition/<int:id>/seasons_and_groups/', views.seasons_and_groups, name='seasons_and_groups'),
    path('teams/', views.team_list, name='teams'),
    path('teams/<int:id>/', views.teams_detail, name='teams_detail'),
    path('players', views.player_list, name='players'),
    path('player/<int:id>/', views.player_detail, name='player_detail'),
    path('games/', views.game_list, name='game_list'),
    path('game/<int:id>/', views.game_detail, name='game_detail'),
    path('standings/', views.standings_table, name='standings_table'),
    path('inscriptions/', views.inscription_list, name='inscription_list'),
    path('inscription/<int:id>/', views.inscription_details, name='inscription_detail'),
    path('edit_player/<int:id>/', views.edit_player, name='edit_player'),
    path('new_competition/', views.new_competition, name='new_competition'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
