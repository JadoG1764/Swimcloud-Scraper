from django.shortcuts import render
from Models import MapCreator
from .models import Races
from Models import MapCreator
from django.utils.text import slugify
from django.shortcuts import redirect


def home_page(request):
    return render(request, "home.html" )

def races_page(request):
    selected_event = request.GET.get("event")
    selected_top = request.GET.get("top")
    races = Races.objects.all()
    if selected_event:
        if selected_event != "All":
            races = races.filter(event=selected_event)
    if selected_top:
        if selected_top != "All":
            races = races.filter(place__range=(1, int(selected_top)))
    return render(request, "Races.html", {'races': races})

def swimmers_page(request):
    return render(request, "swimmers.html")

def swimmers_slug(request, name):
    races = Races.objects.all().filter(name_slug=name)
    formatted_name = ""
    if races:
        formatted_name = races[0].name
    return render(request, "swimmers.html", {'races': races, 'formatted_name': formatted_name})

def teams_slug(request, name):
    races = Races.objects.all().filter(team_slug=name)
    formatted_team = ""
    if races:
        formatted_team = races[0].team
    return render(request, "teams.html", {'races': races, 'formatted_name': formatted_team})


def teams_page(request):
    races = Races.objects.all()
    return render(request, "teams.html", {'races': races})

def swimmer_redirect(request):
    if request.method == 'POST':
        name = request.POST.get('SwimmerName', '')
        slug_name = name.replace(' ', '-').lower()
        return swimmers_slug('swimmers_slug', name=slug_name)
    return redirect('/')

def teams_redirect(request):
    if request.method == 'POST':
        name = request.POST.get('TeamName', '')
        team_name = name.replace(' ', '-').lower()
        return teams_slug('teams_slug', name=team_name)
    return redirect('/')