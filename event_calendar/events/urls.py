from django.urls import path
from django.utils import timezone

from . import views

app_name = "events"
urlpatterns = [
    path("", views.ClosestEventsView.as_view(), name="Closest events"),
    path("all/", views.AllEventsView.as_view(), name="All events"),
    path("ongoing/", views.OngoingEventsView.as_view(), name="Ongoing events"),
    path("past/", views.PastEventsView.as_view(), name="Past events"),
    path("<int:pk>/", views.DetailView.as_view(), name="Detail"),
    path(
        "calendar/<int:month>/<int:year>/",
        views.CalendarView.as_view(),
        name="Calendar",
    ),
    path(
        "calendar/",
        views.CalendarView.as_view(),
        {"month": timezone.now().month, "year": timezone.now().year},
        name="Calendar",
    ),
    path("create/", views.EventCreateView.as_view(), name="Create"),
]
