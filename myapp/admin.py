from django.contrib import admin
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import format_html

from .models import Inscription, Sport, Group, Season, Modality, Competition, Game, Score, Team, Player


class SeasonInline(admin.StackedInline):
    model = Season
    extra = 0


class CompetitionAdmin(admin.ModelAdmin):
    inlines = [SeasonInline]
    list_display = ('name', 'display_seasons', 'sport_list')

    def display_seasons(self, obj):
        seasons = Season.objects.filter(competition=obj)
        return ", ".join([str(season) for season in seasons])

    display_seasons.short_description = 'Temporadas'


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'competition', 'display_modalities', 'display_groups')

    def display_modalities(self, obj):
        modalities = Modality.objects.filter(season=obj)
        return ", ".join([str(modality) for modality in modalities])

    display_modalities.short_description = 'Modality'

    def display_groups(self, obj):
        groups = Group.objects.filter(season=obj)
        return ", ".join([str(group) for group in groups])

    display_groups.short_description = 'Groups'


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1

    def __init__(self, parent_model, admin_site):
        super().__init__(parent_model, admin_site)
        self.parent_obj = None

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self.parent_obj:
            queryset = queryset.filter(team=self.parent_obj)
        return queryset


class TeamInline(admin.TabularInline):
    inlines = [PlayerInline]
    model = Team
    extra = 0


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_players', 'inscription')
    list_editable = ('inscription', )

    def display_players(self, obj):
        players = obj.player_list.all()
        return ', '.join([str(player_list) for player_list in players])

    display_players.short_description = 'Players'


class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [TeamInline]


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'number_player')
    list_display_links = ('name',)


# Register your models here.
admin.site.register(Inscription, InscriptionAdmin)
admin.site.register(Sport)
admin.site.register(Group)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Modality)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Game)
admin.site.register(Score)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
