from django.contrib import admin

from .models import Sport, Group, Season, Competition, Game, Score, Team, Player, PlayerTeamSeason, Inscription, \
    Location, Availability

# Register your models here.
admin.site.register(Sport)
admin.site.register(Group)
admin.site.register(Season)
admin.site.register(Competition)
admin.site.register(Game)
admin.site.register(Score)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(PlayerTeamSeason)
admin.site.register(Inscription)
admin.site.register(Location)
admin.site.register(Availability)
