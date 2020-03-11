from django.urls import path

from . import views

app_name = "events"
urlpatterns = [
    path("", views.ClosestEventsView.as_view(), name="Closest events"),
    path("all/", views.AllEventsView.as_view(), name="All events"),
    path("ongoing/", views.OngoingEventsView.as_view(), name="Ongoing events"),
    path("<int:pk>/", views.DetailView.as_view(), name="Detail"),
]
