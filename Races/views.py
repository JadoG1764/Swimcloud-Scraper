from tkinter.constants import PAGES

from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib.styles import getSampleStyleSheet
from Models import RewriteCCSDB
from .models import Races
from Models import RewriteCCSDB
from django.utils.text import slugify
from django.shortcuts import redirect
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
import io



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

def swimmers_page(request):
    return render(request, "swimmers.html")

def swimmers_slug(request, name):
    races = Races.objects.all().filter(name_slug=name)
    formatted_name = ""
    if races:
        formatted_name = races[0].name
    return render(request, "swimmers.html", {'races': races, 'formatted_name': formatted_name})

def swimmer_redirect(request):
    if request.method == 'POST':
        name = request.POST.get('SwimmerName', '')
        slug_name = slugify(name)
        return swimmers_slug('swimmers_slug', name=slug_name)
    return redirect('/')

def teams_slug(request, name):
    races = Races.objects.all().filter(team_slug=name)
    formatted_team = ""
    if races:
        formatted_team = races[0].team
    return render(request, "teams.html", {'races': races, 'formatted_name': formatted_team})


def teams_page(request):
    races = Races.objects.all()
    return render(request, "teams.html", {'races': races})

def teams_redirect(request):
    if request.method == 'POST':
        name = request.POST.get('TeamName', '')
        team_name = name.replace(' ', '-').lower()
        return teams_slug('teams_slug', name=team_name)
    return redirect('/')

