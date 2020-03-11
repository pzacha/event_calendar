from django.views import generic
from django.utils import timezone

from .models import Event


class EventsView(generic.ListView):
    template_name = "events/events.html"
    context_object_name = "all_events_list"

    def get_queryset(self):
        """Return all upcoming or ongoing events"""
        return Event.objects.filter(end_date__gte=timezone.now()).order_by("start_date")


class DetailView(generic.DetailView):
    model = Event
    template_name = "events/detail.html"


# ongoing events
# show closest events
# show past events
