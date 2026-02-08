import io
from .models import Races
from django.http import HttpResponse
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def pdf_download(request, division):
    # GET filters
    selected_events = request.GET.getlist("events")
    selected_top = request.GET.get("top")

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

    # PDF setup
    buffer = io.BytesIO()
    pdf = BaseDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=12,
        bottomMargin=36,
    )

    frame = Frame(
        pdf.leftMargin,
        pdf.bottomMargin,
        pdf.width,
        pdf.height - 20,  # adjust for header
        id='normal'
    )

    def add_header(canvas, doc):
        canvas.saveState()
        # Text
        canvas.setFont('Helvetica', 16)
        canvas.drawString(36, letter[1] - 30, f"{division} Division Rankings")
        # Image
        header_image_path = "static/viking_logo.jfif"  # adjust to your static path
        try:
            img = Image(header_image_path, width=55, height=52)
            img.drawOn(canvas, 483, letter[1] - 55)  # adjust x, y
        except:
            pass
        canvas.restoreState()

    template = PageTemplate(id='header_template', frames=[frame], onPage=add_header)
    pdf.addPageTemplates([template])

    # PDF elements
    styles = getSampleStyleSheet()
    heading2 = ParagraphStyle(
        'SmallHeading2',
        parent=styles['Heading2'],
        fontSize=12,  # smaller font size
        leading=14,  # line spacing
        spaceAfter=1,
        spaceBefore=1,
    )

    elements = []

    current_event = None
    events_on_page = 0
    current_gender = None

    for race in races:
        # Add a header when the event or gender changes
        if current_gender is not None and current_gender != race.gender:
            elements.append(PageBreak())
            events_on_page = 0

        if race.event != current_event:
            current_event = race.event
            current_gender = race.gender
            events_on_page += 1

            if events_on_page > 2:
                elements.append(PageBreak())
                events_on_page = 1

            elements.append(Spacer(0, 3))
            elements.append(Paragraph(
                f"<b>{race.gender}'s {current_event}</b>",
                heading2
            ))
            elements.append(Spacer(1, 1))

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
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
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