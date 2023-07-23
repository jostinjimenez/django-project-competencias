from django import forms
from .models import Player, Sport, Competition


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'number_player', 'position']


class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ['name', 'type_sport']


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'sport_list', 'is_active']
