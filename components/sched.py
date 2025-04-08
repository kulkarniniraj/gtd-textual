from datetime import datetime, timedelta
from textual.screen import ModalScreen
from textual.widgets import Select, Label, Footer
from textual.app import ComposeResult, App
from textual.containers import Vertical

class SchedPicker(ModalScreen):
    """
    Picker for schedules. A select with options: 
    today, tomorrow, this week,next week, next month, next year
    """
    BINDINGS = [("q,ctrl+s", "exit", "Exit")]

    def compose(self) -> ComposeResult:
        v = Vertical(
            Select(
                [('Today', 'today'),
                 ('Tomorrow', 'tomorrow'),
                 ('This Week', 'this_week'),
                 ('Next Week', 'next_week'),
                 ('Next Month', 'next_month'),
             ('Next Year', 'next_year')],
            id="sched-picker"),
            id="sched-container"
        )
        v.border_title = "Schedule Date"
        yield v
        yield Footer()

    def action_exit(self):
        selected = self.query_one("#sched-picker").value

        if selected == 'today':
            # get today's date, set time to 00:00:00
            sched_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        elif selected == 'tomorrow':
            sched_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        elif selected == 'this_week':
            # before wednesday, set to wednesday, before friday, set to friday, otherwise set to next monday
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if today.weekday() < 2:
                day_delta = 2 - today.weekday()
            elif today.weekday() < 4:
                day_delta = 4 - today.weekday()
            else:
                day_delta = 7 - today.weekday()
            sched_date = today + timedelta(days=day_delta)
        elif selected == 'next_week':
            day_delta = 7 - today.weekday()
            sched_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=day_delta)
        elif selected == 'next_month':
            # get the first day of the next month
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if today.month == 12:   
                next_month = 1
                next_year = today.year + 1
            else:
                next_month = today.month + 1
                next_year = today.year
            sched_date = datetime(next_year, next_month, 1).replace(hour=0, minute=0, second=0, microsecond=0)
        elif selected == 'next_year':
            sched_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, day=1, month=1) + timedelta(days=365)
        else:
            sched_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.dismiss(sched_date)


