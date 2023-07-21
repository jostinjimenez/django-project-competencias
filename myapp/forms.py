from django import forms
from .models import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'number_player', 'position']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a name'}),
            'number_player': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a number'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a position'}),
        }
