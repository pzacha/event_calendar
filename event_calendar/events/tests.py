import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Event


def create_event(event_name, start_days_delta, end_days_delta):
    start = timezone.now() + datetime.timedelta(days=start_days_delta)
    end = timezone.now() + datetime.timedelta(days=end_days_delta)
    return Event.objects.create(name=event_name, start_date=start, end_date=end)


class ClosestEventsViewTests(TestCase):
    def test_closest_events(self):
        """
        Only present 5 closest ongoing or upcoming events.
        """
        create_event("Event5", 4, 5)
        create_event("Event1", -4, -2)
        create_event("Event3", -1, 3)
        create_event("Event2", -2, 1)
        create_event("Event4", 0, 2)
        create_event("Event7", 10, 11)
        create_event("Event6", 8, 12)

        response = self.client.get(reverse("events:Closest events"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["events_list"],
            [
                "<Event: Event2>",
                "<Event: Event3>",
                "<Event: Event4>",
                "<Event: Event5>",
                "<Event: Event6>",
            ],
        )


class AllEventsViewTests(TestCase):
    def test_no_events(self):
        """
        If there are no events, an appropriate message is displayed.
        """
        response = self.client.get(reverse("events:All events"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No events are available.")
        self.assertQuerysetEqual(response.context["events_list"], [])

    def test_present_event(self):
        """
        Present event is displayed on the All events page.
        """
        create_event("Present event", -1, 2)
        response = self.client.get(reverse("events:All events"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["events_list"], ["<Event: Present event>"]
        )

    def test_past_event(self):
        """
        Past event is not displayed on the All events page.
        """
        create_event("Past event", -4, -2)
        response = self.client.get(reverse("events:All events"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No events are available.")
        self.assertQuerysetEqual(response.context["events_list"], [])

    def test_future_and_past(self):
        """
        Future event is displayed on the All events page.
        Past event is not displayed on the All events page.
        """
        create_event("Past event", -4, -2)
        create_event("Future event", 4, 5)
        response = self.client.get(reverse("events:All events"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["events_list"], ["<Event: Future event>"]
        )


class OngoingEventsViewTests(TestCase):
    def test_future_past_and_present(self):
        """
        Only present event is displayed on Ongoing events page.
        """
        create_event("Past event", -4, -2)
        create_event("Present event", -3, 2)
        create_event("Future event", 4, 5)
        response = self.client.get(reverse("events:Ongoing events"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["events_list"], ["<Event: Present event>"]
        )


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

    def test_dates_validation(self):
        """
        Event cannot end before it started.
        """
        start_time = timezone.now() - datetime.timedelta(days=10)
        end_time = start_time + datetime.timedelta(days=-1)
        wrong_event = Event(
            name="Wrong event", start_date=start_time, end_date=end_time
        )
        self.assertRaises(ValidationError, wrong_event.clean)
