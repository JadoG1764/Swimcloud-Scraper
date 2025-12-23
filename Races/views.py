from django.shortcuts import render
from Models import MapCreator
from .models import Races

def home_page(request):
    return render(request, "home.html" )

def races_page(request):
    races = Races.objects.all()
    return render(request, "races.html", {'races': races})

