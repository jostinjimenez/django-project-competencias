from bootstrap_datepicker_plus.widgets import DatePickerInput
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
        fields = ['name', 'date_start', 'date_end', 'sport', 'season', 'genre', 'type_competition',
                  'number_grups', 'is_active']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'date_start': DatePickerInput(format='%Y-%m-%d', options={
                'locale': 'es',
                'showClose': True,
                'showClear': True,
                'showTodayButton': True,
            }, attrs={'class': 'form-control border-2 rounded-pill'}),  # Agregamos la clase 'rounded-pill' aquí
            'date_end': DatePickerInput(format='%Y-%m-%d', options={
                'locale': 'es',
                'showClose': True,
                'showClear': True,
                'showTodayButton': True,
            }, attrs={'class': 'form-control border-2 rounded-pill'}),  # Agregamos la clase 'rounded-pill' aquí
            'genre': forms.Select(attrs={'class': 'form-select border-2 rounded-pill'}),
            'sport': forms.Select(attrs={'class': 'form-select border-2 rounded-pill'}),
            'type_competition': forms.Select(attrs={'class': 'form-select border-2 rounded-pill'}),
            'number_grups': forms.TextInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'season': forms.Select(attrs={'class': 'form-select border-2 rounded-pill'}),
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = PlayerTeamSeason
        fields = ['name', 'city', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['city'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['country'].widget.attrs.update({'class': 'form-select mb-3'})
