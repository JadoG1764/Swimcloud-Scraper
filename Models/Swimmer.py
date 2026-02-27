import json

class Swimmer:

    def __init__(self, name=None, swimmerId=None, eventlist=None, gender=None):
        self.events = {}
        i = 0
        if eventlist is not None:
            while i in range(len(eventlist)):
                if eventlist[i][-3:] == "SCY":
                    self.events[eventlist[i]] = eventlist[i + 1]
                i += 6
        if name is not None:
            self.name = name
        else:
            self.name = "NAME NOT FOUND"
        if swimmerId is not None:
            self.id = swimmerId
        else:
            self.id = "ID NOT FOUND"
        if gender is not None:
            self.gender = gender
        else:
            self.gender = "GENDER NOT FOUND"

    def Print(self):
        print(f"{self.name} is a {self.gender} with the ID number {self.id}")
        for event in self.events:
            print(f"{event}: {self.events[event]}")

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "events": self.events,
            "gender": self.gender
        }

    @classmethod
    def from_dict(cls, json_dict):
        return cls(
            name=json_dict["name"],
            swimmerId=json_dict["id"],
            eventlist=None,
            gender=json_dict["gender"]
        )

    def AddToFile(self):
        #with open("SwimmersTimesCCS.txt", "a", encoding="utf-8") as file:
        with open(f"AllSwimmers.txt", "a", encoding="utf-8") as file:
            file.write(json.dumps(self.to_dict(), indent=4))
