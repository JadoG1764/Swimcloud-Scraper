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
import io



#selected_event = ""
#selected_top = ""


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

def pdf_download(request, division):
    # GET filters
    selected_events = request.GET.getlist("events")
    selected_top = request.GET.get("top")

    # PDF setup
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=18,
        bottomMargin=36,
    )

    # Base queryset
    races = Races.objects.filter(division=division)

    # Filter by events if any selected
    if selected_events:
        races = races.filter(event__in=selected_events)

    # Filter by Top X
    if selected_top:
        try:
            selected_top = int(selected_top)
            races = races.filter(place__lte=selected_top)
        except ValueError:
            selected_top = None

    # PDF elements
    styles = getSampleStyleSheet()
    elements = []

    current_event = None
    events_on_page = 0
    gender_switch = 0

    for race in races:
        # Add a header when the event or gender changes
        if race.event != current_event:
            current_event = race.event
            current_gender = race.gender
            events_on_page += 1

            if events_on_page > 2:
                elements.append(PageBreak())
                events_on_page = 1

            if gender_switch != 1:
                if race.gender == "Women":
                    events_on_page = 1
                    gender_switch = 1
                    elements.append(PageBreak())

            elements.append(Spacer(1, 3))
            elements.append(Paragraph(
                f"<b>{race.gender}'s {current_event}</b>",
                styles["Heading2"]
            ))
            elements.append(Spacer(1, 3))

        # Table row
        row = [
            race.place,
            race.name,
            race.team,
            race.time,
        ]

        table = Table([row], colWidths=[15, 100, 270, 80])

        style = TableStyle([
            ("ALIGN", (0, 0), (0, 0), "LEFT"),  # place
            ("ALIGN", (1, 0), (1, 0), "LEFT"),  # name
            ("ALIGN", (2, 0), (2, 0), "CENTER"),  # team
            ("ALIGN", (3, 0), (3, 0), "RIGHT"),  # time
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ])

        # Highlight team
        if race.team == "Diablo Valley":
            style.add("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")

        table.setStyle(style)
        elements.append(table)

    pdf.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{division}_races.pdf"'
    return response