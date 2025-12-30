import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "ClubSwim.settings"  # <-- MUST match your project settings path
)

django.setup()

from time import sleep
import requests
from bs4 import BeautifulSoup
from Models.Race import Race
from Models import MapCreator

#Declarations
td_text = []
eventNumList = [150, 1100, 1200, 1500, 11000, 250, 2100, 2200, 350, 3100, 3200, 450, 4100, 4200, 5100, 5200, 5400]
genderList = ["M", "F"]
j = 0
#Race.ClearFile("SwimmersTimes.txt") #resets the file
eventMap: dict[int, Race] = {}

#Loops over both genders, all events, up to the top 200 in each event
"""
for gender in genderList:
    for event in eventNumList:
        td_text = []
        eventMap: dict[int, Race] = {}
        for i in range(4): #replace 4 with however many values you want *50, e.g. 10 is top 500.
            url = f"https://www.swimcloud.com/times/iframe/?page={i+1}&region=genericregion_457&orgcode=1&course=Y&hide_gender=0&hide_season=0&event={event}&season=29&age_group=UNOV&gender={gender}"
            data = requests.get(url).text
            soup = BeautifulSoup(data, "html.parser")
            td_text.extend(td.get_text(strip=True) for td in soup.find_all("td")) #adds to the list what we scrape
            sleep(1) #num seconds to sleep to not overload the server
            if len(td_text) % 350 != 0:
                break
        i = 0
        while i in range(len(td_text)): #td_text is a multiple of 6 so guaranteed to not go out of index if we access the first element of the 6
            place = td_text[i]
            name = td_text[i+1]
            team = td_text[i+2]
            meet = td_text[i+3]
            time = td_text[i+4]
            if str(td_text[i+5]).__contains__("NQT"):
                NQT = "True"
            else:
                NQT = "False"
            temp_race = Race(place, name, team, meet, time, event, gender, NQT)
            eventMap[j] = temp_race
            if len(eventMap) == 51 or len(eventMap) == 101 or len(eventMap) == 151:
                if eventMap[j] == eventMap[j-50]:
                    break
            temp_race.AddToFile()

            j += 1 #j is the index in the dictionary
            i += 7 #7 fields to go to the next line in the dictionary
"""
MapCreator.RaceMap()