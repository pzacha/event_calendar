import datetime

from django.db import models
from django.utils import timezone


class Event(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    desc = models.TextField("Event description", blank=True, max_length=1500)

    def __str__(self):
        return self.name

    def status(self):
        if self.start_date > timezone.now():
            return "Upcoming"
        elif self.start_date <= timezone.now() and self.end_date >= timezone.now():
            return "Ongoing"
        else:
            return "Ended"

