import datetime

START_YEAR = 2013  # Only used for the very first run

NOMOSDB_URL = 'http://nomosdb.acme.edu'
NOMOSDB_NAME = 'NomosDB'

# The following is used to sign mails, could also be "The DB Admin Team"
ADMIN_EMAIL = 'chuck.jones@acme.edu'
ADMIN_NAME = 'Chuck Jones'

TEACHING_WEEKS = (
    [(i, 'Week ' + str(i)) for i in range(1, 53)]
)

TEACHING_WEEK_HELPTEXT = (
    'Enter the teaching weeks for the sessions with recorded attendance ' +
    'below. If you need more information, refer to the <a href="http://' +
    'www.canterbury.ac.uk/support/registry/documents/taro/SEP2013toAUG2015' +
    'WeekNumbers.pdf" target="_blank">Week Overview</a> and the <a href="ht' +
    'tp://www.canterbury.ac.uk/support/student-support-and-guidance/term-da' +
    'tes/2014-2015.asp" target="_blank">Term Dates</a> on the CCCU website. '
)

# Automatically fill out the options (see HTML above).
# Always give the name of the option, the first week, the last week
# and the weeks without teaching in the tuple.
TEACHING_WEEK_OPTIONS = {
    1: (
        'Short/Fat, term 1',
        '5',
        '15',
        '9'
    ),
    2: (
        'Short/Fat, term 2',
        '19',
        '29',
        '25'
    ),
    3: (
        'Long/Thin, even weeks',
        '6',
        '28',
        '7,9,11,13,15,16,17,18,19,21,23,25,27'
    ),
    4: (
        'Long/Thin, odd weeks',
        '5',
        '29',
        '6,8,10,12,14,16,17,18,19,20,22,24,26,28'
    )
}

FIRST_WEEK_STARTS = {
    1900: datetime.date(1900, 9, 3), # Leave this in for the tests to work
    2013: datetime.date(2013, 9, 2),
    2014: datetime.date(2014, 9, 1)
}
