from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.http import request

from .utils import Calendar
from .models import Event


class AllEventsView(generic.ListView):
    template_name = "events/events.html"
    context_object_name = "events_list"

    def get_queryset(self):
        """Return all upcoming or ongoing events"""
        return Event.objects.order_by("start_date")


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
            Event.objects.filter(start_date__lte=timezone.now())
            .filter(end_date__gte=timezone.now())
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


class CalendarView(generic.ListView):
    model = Event
    template_name = "events/calendar.html"
    # success_url = reverse_lazy("calendar")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # d = get_date(self.request.GET.get("month", None))
        cal = Calendar(timezone.now().year, timezone.now().month)
        html_cal = cal.formatmonth()
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = context["view"].kwargs["month"] - 1
        context["next_month"] = context["view"].kwargs["month"] + 1
        context["set_year"] = context["view"].kwargs["year"]
        return context
