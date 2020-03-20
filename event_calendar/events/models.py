import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.urls import reverse

from users.models import CustomUser


class Event(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    desc = models.TextField("Event description", blank=True, max_length=1500)
    participants = models.ManyToManyField(CustomUser, related_name="events")

    def __str__(self):
        return self.name

    def status(self):
        if self.start_date > timezone.now():
            return "Upcoming"
        elif self.start_date <= timezone.now() and self.end_date >= timezone.now():
            return "Ongoing"
        else:
            return "Ended"

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError({"end_date": ("Event cannot end before it started.")})

    def get_event_url(self):
        url = reverse("events:Detail", args=[self.id,])
        return '<a href="%s">%s</a>' % (url, str(self.name))

    def get_absolute_url(self):
        return reverse("events:Detail", args=[str(self.id)])

