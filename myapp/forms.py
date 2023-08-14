from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django import forms
from .models import Player, Sport, Competition, PlayerTeamSeason, Team, Season, Location, Availability


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'number_player', 'position', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'number_player': forms.NumberInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'position': forms.TextInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'image': forms.FileInput(attrs={'class': 'form-control border-2 rounded-pill'}),
        }


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
    # Agregamos un nuevo campo para permitir agregar un nuevo deporte
    new_sport_name = forms.CharField(max_length=50, required=False,
                                     widget=forms.TextInput(attrs={'class': 'form-control border-2 rounded-pill'}))

    class Meta:
        model = Competition
        fields = ['name', 'sport', 'new_sport_name', 'genre', 'type_competition', 'is_active']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'genre': forms.Select(attrs={'class': 'form-select border-2 rounded-pill'}),
            'sport': forms.Select(attrs={'class': 'form-select border-2 rounded-pill'}),
            'type_competition': forms.Select(attrs={'class': 'form-select border-2 rounded-pill'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Verificamos si se ingresó un nuevo nombre de deporte
        new_sport_name = self.cleaned_data.get('new_sport_name', '').strip()
        if new_sport_name:
            # Creamos un nuevo deporte
            new_sport = Sport.objects.create(name=new_sport_name)
            instance.sport = new_sport

        if commit:
            instance.save()
        return instance


class TeamForm(forms.ModelForm):
    season = forms.ModelChoiceField(queryset=Season.objects.all(), required=False,
                                    widget=forms.Select(attrs={'class': 'form-control border-2 rounded-pill'}))

    class Meta:
        model = Team
        fields = ['name', 'city', 'country', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'city': forms.TextInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'country': forms.TextInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'image': forms.FileInput(attrs={'class': 'form-control border-2 rounded-pill'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'{field.label} *'


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['name', 'number_grups', 'date_start', 'date_end']

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
            'number_grups': forms.NumberInput(attrs={'class': 'form-control border-2 rounded-pill'}),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'number_seats', 'addres', 'geolocation']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'number_seats': forms.TextInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'addres': forms.TextInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'geolocation': forms.HiddenInput(),
        }


class AvailabilityForm(forms.ModelForm):
    days_available = forms.MultipleChoiceField(
        choices=Availability.DAYS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
    )

    class Meta:
        model = Availability
        fields = ['days_available', 'opening_time', 'closing_time', 'date']

        widgets = {
            'opening_time': TimePickerInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'closing_time': TimePickerInput(attrs={'class': 'form-control border-2 rounded-pill'}),
            'date': DatePickerInput(format='%Y-%m-%d', options={
                'locale': 'es',
                'showClose': True,
                'showClear': True,
                'showTodayButton': True,
            }, attrs={'class': 'form-control border-2 rounded-pill'}),
        }
