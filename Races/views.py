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
    races = Races.objects.all()
    if selected_event:
        if selected_event != "All":
            races = races.filter(event=selected_event)
    return render(request, "Races.html", {'races': races})

def swimmers_page(request):
    return render(request, "swimmers.html")

def swimmers_slug(request, name):
    formatted_name = name.replace('-', ' ').title()
    races = Races.objects.all()
    if formatted_name:
        races = races.filter(name=formatted_name)
    return render(request, "swimmers.html", {'races': races, 'formatted_name': formatted_name})

def teams_page(request):
    races = Races.objects.all()
    return render(request, "teams.html", {'races': races})

def swimmer_redirect(request):
    if request.method == 'POST':
        name = request.POST.get('SwimmerName', '')
        slug_name = name.replace(' ', '-').lower()
        return swimmers_slug('swimmers_slug', name=slug_name)
    return redirect('/')