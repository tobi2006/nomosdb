import datetime
from main.unisettings import FIRST_WEEK_STARTS
from main.models import Setting


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
        current_year = int(Setting.objects.get(name='current_year').value)
        if chosen_date:
            today = chosen_date
        else:
            today = datetime.date.today()
        previous_monday = today - datetime.timedelta(days=today.weekday())
        try:
            day = FIRST_WEEK_STARTS[current_year]
            week_number = False
            for week in range(1, 53):
                if day == previous_monday:
                    week_number = week
                    break
                else:
                    day += datetime.timedelta(days=7)
        except KeyError:
            week_number = False
    except Setting.DoesNotExist:
        week_number = False
    return week_number


def week_starting_date(number, year='current'):
    try:
        if year == 'current':
            current_year = int(Setting.objects.get(name="current_year").value)
        else:
            year = int(year)
        first_day = FIRST_WEEK_STARTS[year]
        week_number = int(number) - 1
        difference = week_number * 7
        week_starting_date = first_day + datetime.timedelta(days=difference)
    except Setting.DoesNotExist:
        week_starting_date = None
    return week_starting_date


def formatted_date(raw_date):
    """Returns a proper date string

    This returns a string of the date in British Format.
    If the date field was left blank, an empty string is returned.
    """
    if raw_date is None:
        result = ''
    else:
        result = (
            str(raw_date.day) + '/' + str(raw_date.month) + '/' +
            str(raw_date.year))
    return result


def academic_year_string(year):
    """Returns the academic year starting with the given year

    academic_year_string(2013) will return '2013/14'"""
    year = int(year)
    second = str(year + 1)
    year = str(year)
    if len(year) == 1:
        year = '0' + year
    if len(second) == 1:
        second = '0' + second
    returnstr = (
        year +
        '/' +
        second[-2] +
        second[-1]
    )
    return returnstr
