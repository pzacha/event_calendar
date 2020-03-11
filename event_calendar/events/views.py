from django.views import generic
from django.utils import timezone

from .models import Event


class AllEventsView(generic.ListView):
    template_name = "events/events.html"
    context_object_name = "events_list"

    def get_queryset(self):
        """Return all upcoming or ongoing events"""
        return Event.objects.filter(end_date__gte=timezone.now()).order_by("start_date")


class ClosestEventsView(generic.ListView):
    template_name = "events/events.html"
    context_object_name = "events_list"

    def get_queryset(self):
        """Return 5 closest events"""
        return Event.objects.filter(end_date__gte=timezone.now()).order_by(
            "start_date"
        )[:5]


class OngoingEventsView(generic.ListView):
    template_name = "events/events.html"
    context_object_name = "events_list"

    def get_queryset(self):
        """Return all ongoing events"""
        return (
            Event.objects.filter(start_date__gte=timezone.now())
            .filter(end_date__lte=timezone.now())
            .order_by("start_date")
        )


class PastEventsView(generic.ListView):
    template_name = "events/events.html"
    context_object_name = "events_list"

    def get_queryset(self):
        """Return all past events"""
        return Event.objects.filter(end_date__lte=timezone.now()).order_by("start_date")


class DetailView(generic.DetailView):
    model = Event
    template_name = "events/detail.html"


# ongoing events
# show closest events
# show past events
