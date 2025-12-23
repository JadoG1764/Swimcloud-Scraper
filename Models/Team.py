from .Swimmer import Swimmer
class Team:
    def __init__(self, teamname = None):
        self.swimmers: dict[str, Swimmer] = {}
        self.teamName = teamname


    def AddSwimmer(self, swimmer):
        self.swimmers[swimmer.name] = swimmer
        if self.teamName is None:
            self.teamName = swimmer.team

    def PrintSwimmers(self):
        for name, swimmer in self.swimmers.items():
            print(name)

