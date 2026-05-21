from django.http import HttpResponse
from django.shortcuts import render
from .models import Races
from django.utils.text import slugify
from django.shortcuts import redirect



def home_page(request):
    return render(request, "home.html" )

def division_page(request, division):
    return render(request, "division.html", {"division": division,})

def races_page(request, division):
    # GET parameters
    selected_events = request.GET.getlist("events")
    selected_top = request.GET.get("top")

    # Base queryset
    races = Races.objects.filter(division=division)

    # Filter by selected events (checkboxes)
    if selected_events:
        races = races.filter(event__in=selected_events)

    # Filter by Top X
    if selected_top:
        try:
            selected_top = int(selected_top)
            races = races.filter(place__lte=selected_top)
        except ValueError:
            selected_top = None

    context = {
        "division": division,
        "races": races,
        "selected_events": selected_events,
        "selected_top": selected_top,
    }

    return render(request, "Races.html", context)

def swimmers_page(request, division):
    swimmers = Races.objects.filter(division=division).values('name', 'name_slug').distinct()
    return render(request, "Swimmers.html", {
        'swimmers': swimmers,
        'division': division,
    })

def swimmers_slug(request, division, name):
    races = Races.objects.all().filter(division=division, name_slug=name)
    formatted_name = ""
    if races:
        formatted_name = races[0].name
    return render(request, "Swimmers.html", {
        'races': races,
        'formatted_name': formatted_name,
        'division': division,
    })

def swimmer_redirect(request, division):
    if request.method == 'POST':
        name = request.POST.get('SwimmerName', '')
        if name:
            slug_name = slugify(name)
            return redirect('swimmers_slug', division=division, name=slug_name)
    return redirect('swimmers_page', division=division)

def teams_slug(request, division, name):
    sort = request.GET.get('sort', 'place')
    if sort not in ('place', '-place'):
        sort = 'place'
    races = Races.objects.filter(division=division, team_slug=name).order_by(sort)
    formatted_team = ""
    if races:
        formatted_team = races[0].team
    return render(request, "teams.html", {
        'races': races,
        'formatted_name': formatted_team,
        'division': division,
        'sort': sort,
    })


def teams_page(request, division):
    teams = Races.objects.filter(division=division).values('team', 'team_slug').distinct()
    return render(request, "teams.html", {'teams': teams, 'division': division})


def team_redirect(request, division):
    if request.method == 'POST':
        name = request.POST.get('TeamName', '')
        if name:
            slug_name = slugify(name)
            return redirect('teams_slug', division=division, name=slug_name)
    return redirect('teams_page', division=division)

