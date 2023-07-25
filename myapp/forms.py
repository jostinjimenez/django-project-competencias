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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['type_sport'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['image'].widget.attrs.update({'class': 'form-control mb-3'})


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'sport', 'is_active', 'awards', 'rules_and_regulations']

    def __init__(self, *args, **kwargs):
        super(CompetitionForm, self).__init__(*args, **kwargs)

        # Agregar clases de Bootstrap a los campos del formulario
        self.fields['name'].widget.attrs['class'] = 'form-control border-2 rounded-pill'
        self.fields['sport'].widget.attrs['class'] = 'form-select border-2 rounded-pill'
        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'
        self.fields['awards'].widget.attrs['class'] = 'form-control border-2 rounded-pill'
        self.fields['rules_and_regulations'].widget.attrs['class'] = 'form-control border-2'
