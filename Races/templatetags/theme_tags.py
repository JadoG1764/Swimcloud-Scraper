from django import template

register = template.Library()

# Maps a division to the CSS body theme class used in templates/base.html.
# CCS uses the University of Utah (Utes) palette; CCCAA and Big 8 use the
# DVC Vikings palette. Anything else (e.g. the home / division-list pages,
# which have no division in context) falls back to the neutral theme.
THEME_MAP = {
    "CCS": "theme-utes",
    "CCCAA": "theme-vikings",
    "Big 8": "theme-vikings",
}


@register.filter
def division_theme(division):
    return THEME_MAP.get(division, "theme-neutral")
