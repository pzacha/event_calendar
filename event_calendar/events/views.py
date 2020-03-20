from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.http import request

from bootstrap_datepicker_plus import DateTimePickerInput

from .utils import Calendar
from .models import Event


class AllEventsView(generic.ListView):
    template_name = "events/events.html"
    context_object_name = "events_list"

    def get_queryset(self):
        """Return all upcoming or ongoing events"""
        return Event.objects.order_by("start_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "All events"
        return context


class ClosestEventsView(generic.ListView):
    template_name = "events/events.html"
    context_object_name = "events_list"

    def get_queryset(self):
        """Return 5 closest events"""
        return Event.objects.filter(end_date__gte=timezone.now()).order_by(
            "start_date"
        )[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Closest events"
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ongoing events"
        return context


class PastEventsView(generic.ListView):
    template_name = "events/events.html"
    context_object_name = "events_list"

    def get_queryset(self):
        """Return all past events"""
        return Event.objects.filter(end_date__lte=timezone.now()).order_by("start_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Past events"
        return context


class DetailView(generic.DetailView):
    model = Event
    template_name = "events/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["object"].name
        return context


class CalendarView(generic.ListView):
    model = Event
    template_name = "events/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Calendar"

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


class EventCreateView(generic.edit.CreateView):
    model = Event
    template_name = "events/create.html"
    fields = ["name", "start_date", "end_date"]

    def get_form(self):
        form = super().get_form()
        form.fields["start_date"].widget = DateTimePickerInput()
        form.fields["end_date"].widget = DateTimePickerInput()
        return form
