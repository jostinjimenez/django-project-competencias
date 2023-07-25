from django import forms
from .models import Player, Sport, Competition, PlayerTeamSeason


class CustomPlayerForm(forms.ModelForm):
    # Agregar campos adicionales para Player
    player_name = forms.CharField(max_length=50)
    number_player = forms.IntegerField()
    position = forms.CharField(max_length=50)

    class Meta:
        model = PlayerTeamSeason
        fields = ['player', 'team', 'season']

    def save(self, commit=True):
        # Obtener los valores de los campos adicionales para Player
        player_name = self.cleaned_data['player_name']
        number_player = self.cleaned_data['number_player']
        position = self.cleaned_data['position']

        # Crear un objeto Player
        player = Player(name=player_name, number_player=number_player, position=position)

        # Guardar el objeto Player antes de guardarlo en PlayerTeamSeason
        if commit:
            player.save()

        # Obtener el objeto Player creado y establecerlo en PlayerTeamSeason
        self.instance.player = player

        # Llamar al método save de forms.ModelForm para guardar PlayerTeamSeason
        return super().save(commit=commit)


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'number_player', 'position']


class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ['name', 'type_sport', 'image']


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'sport_list', 'is_active']
