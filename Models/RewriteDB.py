import os
import django
import re
from pathlib import Path

from django.utils.text import slugify


def rewrite_ccs_db(division=None):
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "ClubSwim.settings"
    )
    django.setup()

    from Models.Race import Race
    from Races.models import Races

    base_dir = Path(__file__).resolve().parents[1]
    file_path = None

    if division == "CCCAA":
        file_path = base_dir / "Data" / "SwimmerTimesCCCAA.txt"
        Races.objects.filter(division="CCCAA").delete()

    elif division == "CCS":
        file_path = base_dir / "Data" / "SwimmersTimesCCS.txt"
        Races.objects.filter(division="CCS").delete()

    else:
        raise ValueError(f"Unknown division: {division}")


    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()


    items = re.split(r"[;\n]", data)
    i = 0

    while i < len(items) - 8:
        race = Race(
            items[i],
            items[i + 1],
            items[i + 2],
            items[i + 3],
            items[i + 4],
            items[i + 5],
            items[i + 6],
            items[i + 7],
            items[i + 8],
        )

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
            division=race.division,
        )

        i += 9


if __name__ == "__main__":
    while (True):
        print("What database do you want to update?")
        print("1.CCCAA")
        print("2.CCS")
        print("3.All")
        print("To exit type 'exit'")
        db = input("Enter your choice: ")
        if db == "1":
            rewrite_ccs_db("CCCAA")
            break
        elif db == "2":
            rewrite_ccs_db("CCS")
            break
        elif db == "3":
            rewrite_ccs_db("CCCAA")
            rewrite_ccs_db("CCS")
            break
        elif db == "exit":
            break
        else:
            print("Invalid choice, Enter 1-3 or type exit to exit")

