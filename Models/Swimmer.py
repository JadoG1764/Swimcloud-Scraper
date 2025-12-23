from .Race import Race

class Swimmer:
    def __init__(self, name = None, team = None, gender = None):
        self.races: dict[str, Race] = {}
        self.name = name
        self.team = team
        self.gender = gender

    def AddRace(self, race):
        self.races[race.event] = race
        if self.name is None:
            self.name = race.name
        if self.team is None:
            self.team = race.team
        if self.gender is None:
            self.gender = race.gender

    def PrintRaces(self):
        for race in self.races.values():
            print(f"{self.name} swims for {self.team} and went {race.time} in the {self.gender}'s {race.event} ranking {race.place} in the nation")

