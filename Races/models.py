from django.db import models
from django.utils.text import slugify

class Races(models.Model):
    place = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    team = models.CharField(max_length=120)
    meet = models.CharField(max_length=120)
    time = models.CharField(max_length=120)
    event = models.CharField(max_length=120)
    gender = models.CharField(max_length=120)
    nqt = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.event})"
