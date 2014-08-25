import datetime
from nomosdb.unisettings import FIRST_WEEK_STARTS
from main.models import Settings


def week_dict(year):
    """Returns a dictionary of all weeks for the academic year

    This needs to be modified to fit your institution's week calendar.
    It needs to be a function because the institutions' ways of counting
    weeks differ strongly (some count all 52 weeks of the year, some
    only teaching weeks etc).
    The current function assumes that ALL weeks are counted.
    """
    year = int(year)
    all_weeks = {}
    day = FIRST_WEEK_STARTS[year]
    for i in range(1, 53):
        all_weeks[i] = current_date
        day += datetime.timedelta(days=7)
    return all_weeks


def week_number(chosen_date=False):
    """Returns the current week number"""
    try:
        current_year = int(Settings.objects.get(name='current_year').value)
        if chosen_date:
            today = chosen_date
        else:
            today = datetime.date.today()
        previous_monday = today - datetime.timedelta(days=today.weekday())
        day = FIRST_WEEK_STARTS[current_year]
        week_number = None
        for week in range(1, 53):
            if day == previous_monday:
                week_number = week
                break
            else:
                day += datetime.timedelta(days=7)
    except Settings.DoesNotExist:
        week_number = None
    return week_number
