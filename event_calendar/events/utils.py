from datetime import datetime, timedelta
from calendar import HTMLCalendar

from .models import Event


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super().__init__()

    def formatday(self, day, events):
        if day != 0:
            current_day = datetime(self.year, self.month, day)
            events_per_day = events.filter(
                start_date__lte=(current_day + timedelta(days=1))
            ).filter(end_date__gte=current_day)
            event_html = ""
            for event in events_per_day:
                event_html += event.get_event_url() + "<br>"

            return f"<td><span class='date'>{day}</span><ul> {event_html} </ul></td>"
        return "<td></td>"

    def formatweek(self, theweek, events):
        week_html = "".join(self.formatday(d, events) for (d, weekday) in theweek)
        return f"<tr> {week_html} </tr>"

    def formatmonth(self):
        events = (
            Event.objects.filter(start_date__year=self.year)
            .filter(start_date__month__lte=self.month)
            .filter(end_date__month__gte=self.month)
        )
        cal = f'<table border="4" cellpadding="20" cellspacing="0" class="calendar">\n'
        cal += f"{self.formatmonthname(self.year, self.month)}\n"
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, events)}\n"
        return cal
