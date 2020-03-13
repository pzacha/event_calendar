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
        m = context["view"].kwargs["month"]
        y = context["view"].kwargs["year"]

        cal = Calendar(y, m)
        html_cal = cal.formatmonth()
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = m - 1
        context["next_month"] = m + 1
        context["next_year"] = y
        context["prev_year"] = y
        if m == 12:
            context["next_month"] = 1
            context["next_year"] = y + 1
        elif m == 1:
            context["prev_month"] = 12
            context["prev_year"] = y - 1
        return context
