from .Race import Race
from .Swimmer import Swimmer
from .Team import Team
from pathlib import Path
from Races.models import Races
import re

racesMap: dict[int, Race] = {}
swimmersMap: dict[str, Swimmer] = {}
teamsMap: dict[str, Team] = {}

BASE_DIR = Path(__file__).resolve().parents[1]
file_path = BASE_DIR / "Data" / "SwimmersTimes.txt"
def RaceMap():
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
            defaults={'nqt': race.nqt}
        )
        i += 8
        j += 1

def SwimmerMap():
    for index, race in racesMap.items():
        if race.name not in swimmersMap:
            swimmersMap[race.name] = Swimmer()
            swimmersMap[race.name].AddRace(race)
        else:
            swimmersMap[race.name].AddRace(race)
    return swimmersMap

def TeamMap():
    for name, swimmer in swimmersMap.items():
        if swimmer.team not in teamsMap:
            teamsMap[swimmer.team] = Team()
            teamsMap[swimmer.team].AddSwimmer(swimmer)
        else:
            teamsMap[swimmer.team].AddSwimmer(swimmer)
    return teamsMap