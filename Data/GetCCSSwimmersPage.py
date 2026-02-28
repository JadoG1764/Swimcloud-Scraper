from time import sleep
import requests
from bs4 import BeautifulSoup
from Models.Race import Race
import json
from Models.Swimmer import Swimmer


def sec_to_minute(seconds):
    minutes = int(seconds // 60)
    seconds %= 60

    if minutes != 0:
        if seconds < 10:
            time = f"{minutes}:0{seconds:.2f}"
        else:
            time = f"{minutes}:{seconds:.2f}"
    else:
        time = f"{seconds}"

    return time

def build_scy_events(results):
    events = {}

    stroke_map = {
        "1": "Free",
        "2": "Back",
        "3": "Breast",
        "4": "Fly",
        "5": "IM"
    }

    for swim in results:
        minutes = 0
        distance = swim["eventdistance"]
        stroke = stroke_map.get(swim["eventstroke"], "Unknown")
        time = sec_to_minute(float(swim["eventtime"]))

        key = f"{distance} {stroke} SCY"

        events[key] = time

    return events

def get_gender(results):
    for swim in results:
        if "eventgender" in swim and swim["eventgender"]:
            return swim["eventgender"]
    return "GENDER NOT FOUND"


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}



#Declarations
td_text = []
eventNumList = [150, 1100, 1200, 1500, 11000, 250, 2100, 2200, 350, 3100, 3200, 450, 4100, 4200, 5100, 5200, 5400]
genderList = ["M", "F"]
j = 0
counter = 0
Race.ClearFile("SwimmersTimesCCS.txt") #resets the file
eventMap: dict[int, Race] = {}

url = f"https://www.swimcloud.com/times/iframe/?page=1&region=genericregion_457&orgcode=1&course=Y&hide_gender=0&hide_season=0&event=150&season=29&age_group=UNOV&gender=F"
data = requests.get(url).text
soup = BeautifulSoup(data, "html.parser")
for td in soup.find_all("td"):
    if counter == 1:
        a = td.find("a")
        name = a.find(string=True, recursive=False).strip()
        swimmer_id = a["href"].split("/")[-1]
        swimmerurl = f"https://www.swimcloud.com/api/swimmers/{swimmer_id}/profile_fastest_times/"
        swimmerdata = requests.get(swimmerurl, headers=headers).text
        swimmersoup = BeautifulSoup(swimmerdata, "html.parser")

        print(name, swimmer_id)
        results = json.loads(swimmersoup.prettify())
        gender = get_gender(results)
        scy_results = [r for r in results if r.get("eventcourse") == "Y"]
        scy_events = build_scy_events(scy_results)

        swimmer = Swimmer(
            name=name,
            swimmerId=int(swimmer_id),
            gender=gender,
            events=scy_events
        )

        swimmer.printSwimmer()

    else:
        print(td.text)
    print("-------------------------------------")
    if counter == 6:
        counter = 0
    else:
        counter += 1
    sleep(5)



