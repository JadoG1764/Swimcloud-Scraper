import django
import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "ClubSwim.settings"  # <-- MUST match your project settings path
)

django.setup()

from django.utils.text import slugify
from Models.Race import Race
from pathlib import Path
from Races.models import Races
import re

BASE_DIR = Path(__file__).resolve().parents[1]
division = "CCCAA"

if division == "CCCAA":
    file_path = BASE_DIR / "DataCCCAA" / "SwimmerTimesCCCAA.txt"

    Races.objects.filter(division="CCCAA").delete()
elif division == "CCS":
    file_path = BASE_DIR / "Data" / "SwimmersTimesCCS.txt"

    Races.objects.filter(division="CCS").delete()

with open(file_path, "r", encoding="utf-8") as file:
    #values separated by ;
    data = file.read()

# declarations
items = re.split(r'[;\n]', data)
i, j = 0, 0

while i in range(len(items) - 1):
    race = Race(items[i], items[i + 1], items[i + 2], items[i + 3], items[i + 4], items[i + 5], items[i + 6], items[i + 7], items[i+8])
    Races.objects.get_or_create(
        place=race.place,
        name=race.name,
        team=race.team,
        meet=race.meet,
        time=race.time,
        event=race.event,
        gender=race.gender,
        nqt=race.nqt,
        name_slug=slugify(race.name),
        meet_slug=slugify(race.meet),
        team_slug=slugify(race.team),
        division=race.division
    )
    i += 9
    j += 1
