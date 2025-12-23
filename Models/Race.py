from .NQT import *

cuts = NQT()

#passes in with SwimCloud event format e.g. 1100 and finds the corresponding event in english terms
def FindEvent(event):
    return NQT().EVENT_NAMES.get(event, event)
#passes in a 'M' or 'W' and returns either Men, Women
def FindGender(gender):
    if gender == "M":
        return "Men"
    elif gender == "F":
        return "Women"
    else:
        return gender

def MinutesToSeconds(time):
    if ":" in time:
        minutes, seconds = map(float, time.split(":"))
    else:
        seconds = float(time)
        minutes = 0
    return minutes * 60 + seconds
#Class that holds each swimmer per event, each swimmer can only have 1 event but there might be times when a
#swimmer that appears on more than one event has duplicate objects
class Race:
    def __init__(self, place = None, name = None, team = None, meet = None, time = None, event = None, gender = None, nqt = False):
        self.place = place
        if name is None:
            print(name)
            self.name = "Empty Name"
        else:
            self.name = name.replace(team, "")
        self.team = team
        self.meet = meet
        self.time = time
        if event is None:
            self.event = "Empty Event"
        else:
            self.event = FindEvent(event)
        if gender is None:
            self.gender = "Empty Gender"
        else:
            self.gender = FindGender(gender)
        if nqt == "False":
            if self.gender == "Men":
                if MinutesToSeconds(self.time) < cuts.nqtMens[self.event]:
                    self.nqt = True
                else:
                    self.nqt = False
            else:
                if MinutesToSeconds(self.time) < cuts.nqtWomen[self.event]:
                    self.nqt = True
                else:
                    self.nqt = False
        else:
            self.nqt = True

    def PrintValues(self):
        if self.nqt:
            print(f"{self.place}: {self.name} Swims for {self.team} and went {self.time} at {self.meet} in the {self.gender}'s {self.event} and has NQT")
        else:
            print(
                f"{self.place}: {self.name} Swims for {self.team} and went {self.time} at {self.meet} in the {self.gender}'s {self.event}")
    def AddToFile(self):
        with open("SwimmersTimes.txt", "a", encoding="utf-8") as file:
            file.write(f"{self.place};{self.name};{self.team};{self.meet};{self.time};{self.event};{self.gender};{self.nqt}\n")

    def __eq__(self, other):
        if not isinstance(other, Race):
            return NotImplemented
        return self.place == other.place and self.name == other.name and self.team == other.team and self.meet == other.meet and self.time == other.time and self.event == other.event and self.gender == other.gender and self.nqt == other.nqt

    def CompareTeams(self, team1, team2):
        if self.team == team1 or self.team == team2:
            Race.PrintValues(self)

    @staticmethod
    def SortByPlace(races_map):
        return sorted(races_map.values(), key=lambda r: int(r.place))

    @staticmethod
    def ClearFile(text):
        with open(text, "w") as _:
            pass


