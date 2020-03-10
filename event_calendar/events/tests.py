import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Event


class EventModelTests(TestCase):
    def test_status_with_upcoming_event(self):
        """
        status() returns 'Upcoming' if the start_date of the event is in the future.
        """
        start_time = timezone.now() + datetime.timedelta(days=10)
        end_time = start_time + datetime.timedelta(days=1)
        future_event = Event(
            name="Future event", start_date=start_time, end_date=end_time
        )
        self.assertIs(future_event.status(), "Upcoming")

    def test_status_with_ongoing_event(self):
        """
        status() returns 'Ongoing' if the current time is between start_date and end_date (including these dates).
        """
        start_time = timezone.now() - datetime.timedelta(hours=4)
        end_time = start_time + datetime.timedelta(hours=6)
        present_event = Event(
            name="Present event", start_date=start_time, end_date=end_time
        )
        self.assertIs(present_event.status(), "Ongoing")
        present_event.start_date = timezone.now()
        present_event.end_date = timezone.now()
        self.assertIs(present_event.status(), "Ongoing")

    def test_status_with_past_event(self):
        """
        status() returns 'Ended' if the start_date of the event is in the past
        """
        start_time = timezone.now() - datetime.timedelta(days=10)
        end_time = start_time + datetime.timedelta(days=1)
        past_event = Event(name="Past event", start_date=start_time, end_date=end_time)
        self.assertIs(past_event.status(), "Ended")

