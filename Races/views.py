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



selected_event = ""
selected_top = ""


def home_page(request):
    return render(request, "home.html" )

def CCCAA_page(request):
    return render(request, "CCCAA.html")

def CCS_page(request):
    return render(request, "CCS.html")

def CCS_races_page(request):
    global selected_event
    global selected_top

    if not request.GET.get("event"):
        selected_top = request.GET.get("top")
    if not request.GET.get("top"):
        selected_event = request.GET.get("event")

    races = Races.objects.filter(division="CCS")
    if selected_event:
        if selected_event != "All":
            races = races.filter(event=selected_event)
    if selected_top:
        if selected_top != "All":
            races = races.filter(place__range=(1, int(selected_top)))
    return render(request, "CCS_Races.html", {'races': races, 'selected_event': selected_event, 'selected_top': selected_top})

def CCCAA_races_page(request):
    global selected_event
    global selected_top

    if not request.GET.get("event"):
        selected_top = request.GET.get("top")
    if not request.GET.get("top"):
        selected_event = request.GET.get("event")

    races = Races.objects.filter(division="CCCAA")
    if selected_event:
        if selected_event != "All":
            races = races.filter(event=selected_event)
    if selected_top:
        if selected_top != "All":
            races = races.filter(place__range=(1, int(selected_top)))
    return render(request, "CCCAA_Races.html", {'races': races, 'selected_event': selected_event, 'selected_top': selected_top})

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
    #temporarily made to print with top 20
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=18,
        bottomMargin=36,
    )
    races = Races.objects.filter(division=division, place__lte=20)

    styles = getSampleStyleSheet()
    elements = []

    current_event = None
    events_on_page = 0
    gender_switch = 0

    for race in races:
        # Add a header when the event changes
        if race.event != current_event:
            current_event = race.event
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
                f"<b>{current_event}</b>",
                styles["Heading2"]
            ))
            elements.append(Spacer(1, 3))

        # One-row table per race
        row = [
            race.place,
            race.name,
            race.team,
            race.time,
        ]

        table = Table(
            [row],
            colWidths=[20, 100, 270, 80]
        )

        style = TableStyle([
            ("ALIGN", (0, 0), (0, 0), "LEFT"),    # place
            ("ALIGN", (1, 0), (1, 0), "LEFT"),   # name
            ("ALIGN", (2, 0), (2, 0), "CENTER"),  # team
            ("ALIGN", (3, 0), (3, 0), "RIGHT"),   # time

            # Vertical centering
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            # Padding (controls row height)
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ])

        if race.team == "Diablo Valley":
            # 0 = first col, 3 = fourth col
            style.add("FONTNAME", (0, 0), (3, 0), "Helvetica-Bold")

        table.setStyle(style)
        elements.append(table)

    pdf.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="races.pdf"'
    return response
