from django.utils.text import slugify

from .Race import Race
from pathlib import Path
from Races.models import Races
import re

BASE_DIR = Path(__file__).resolve().parents[1]
file_path = BASE_DIR / "Data" / "SwimmersTimes.txt"
def RaceMap():
    Races.objects.all().delete()
    with open(file_path, "r", encoding="utf-8") as file:
        #values seperated by ;
        data = file.read()

    # declarations
    items = re.split(r'[;\n]', data)
    i, j = 0, 0

    while i in range(len(items) - 1):
        race = Race(items[i], items[i + 1], items[i + 2], items[i + 3], items[i + 4], items[i + 5], items[i + 6], items[i + 7])
        Races.objects.get_or_create(
            place=race.place,
            name=race.name,
            team=race.team,
            meet=race.meet,
            time=race.time,
            event=race.event,
            gender=race.gender,
            nqt=race.nqt,
            slug=slugify(race.name)
        )
        i += 8
        j += 1
