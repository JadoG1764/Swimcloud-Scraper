from django.shortcuts import render
from Models import MapCreator
from .models import Races
from Models import MapCreator


def home_page(request):
    return render(request, "home.html" )

def races_page(request):
    races = Races.objects.all()
    return render(request, "races.html", {'races': races})

def swimmers_page(request):
    races = Races.objects.all()
    return render(request, "swimmers.html", {'races': races})

def teams_page(request):
    races = Races.objects.all()
    return render(request, "teams.html", {'races': races})