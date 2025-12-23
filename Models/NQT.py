import json
from pathlib import Path

EVENT_NAMES = {
            150: "50 Free",
            1100: "100 Free",
            1200: "200 Free",
            1500: "500 Free",
            11000: "1000 Free",
            250: "50 Back",
            2100: "100 Back",
            2200: "200 Back",
            350: "50 Breast",
            3100: "100 Breast",
            3200: "200 Breast",
            450: "50 Fly",
            4100: "100 Fly",
            4200: "200 Fly",
            5100: "100 IM",
            5200: "200 IM",
            5400: "400 IM",
        }

def FindEvent(event):
    return EVENT_NAMES.get(event, event)
def FindGender(gender):
    if gender == "M":
        return "Men"
    elif gender == "F":
        return "Women"
    else:
        return gender
def is_not_int(s):
    try:
        int(s)
        return False
    except ValueError:
        return True
def CreateDict():

    nqt_Times_Womens: dict[str, float] = {}
    nqt_Times_Mens: dict[str, float] = {}

    BASE_DIR = Path(__file__).resolve().parents[1]
    file_path = BASE_DIR / "Data" / "NQT.txt"

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i in data["age_groups"]:
        if len(i["timestandards"]) >= 1:
            event = FindEvent(int(i["meetevent"]["eventstroke"] + str(i["meetevent"]["eventdistance"])))
            time = i["timestandards"][0]["time"]
            gender = FindGender(i["meetevent"]["eventgender"])
            if is_not_int(event):
                if gender == "Men":
                    nqt_Times_Mens[event] = float(time)
                else:
                    nqt_Times_Womens[event] = float(time)
    return nqt_Times_Womens, nqt_Times_Mens
class NQT:
    def __init__(self):
        self.nqtWomen, self.nqtMens = CreateDict()
        self.EVENT_NAMES = EVENT_NAMES







