class Swimmer:
    def __init__(self, name, swimmerId, gender, events=None):
        self.name = name
        self.id = swimmerId
        self.gender = gender
        self.events = events or {}

    def printSwimmer(self):
        print(f"{self.name} is a {self.gender} with the ID number {self.id}")
        for event, time in self.events.items():
            print(f"{event}: {time}")

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "gender": self.gender,
            "events": self.events
        }