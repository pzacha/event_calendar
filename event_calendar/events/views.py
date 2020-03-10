from django.views import generic

from .models import Event


class EventsView(generic.ListView):
    template_name = "events/events.html"
    context_object_name = "all_events_list"

    def get_queryset(self):
        """Return all upcoming or ongoing events"""
        return Event.objects.order_by("start_date")

    # Do not show past events


class DetailView(generic.DetailView):
    model = Event
    template_name = "events/detail.html"


# ongoing events
# show closest events
# show past events
