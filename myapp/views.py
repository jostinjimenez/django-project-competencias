from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .forms import PlayerForm
from .models import Competition, Season


# Create your views here.
def seasons(request):
    seasons = Season.objects.all()
    return render(request, 'season.html', {'seasons': seasons})



def seasons(request):
    seasons = Season.objects.all()
    return render(request, 'season.html', {'seasons': seasons})


def new_player(request):
    form = PlayerForm()
    return render(request, 'new_player.html', {'form': form})


def competition_detail(request, id):
    competition = get_object_or_404(Competition, pk=id)
    return render(request, 'competition_detail.html', {'competition': competition})


def home(request):
    return render(request, 'home.html')


# Función para registrar un usuario
def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })
        return render(request, 'signin.html', {
            'form': UserCreationForm,
            'error': 'Passwords did not match'
        })


# Función para cerrar sesión
@login_required
def signout(request):
    logout(request)
    return redirect('home')


# Función para iniciar sesión
def signin(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password incorrect'
            })
        else:
            login(request, user)
            return redirect('home')


def competitions(request):
    competitions = Competition.objects.all()
    return render(request, 'competitions.html', {'competitions': competitions})

