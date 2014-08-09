import datetime
from django.core.urlresolvers import reverse
from django.db import models

ACADEMIC_YEARS = (
    [(i, str(i) + "/" + str(i+1)[-2:]) for i in range(2010, 2025)]
)

TEACHING_WEEKS = (
    [(i, 'Week ' + str(i)) for i in range(1, 53)]
)


def this_year():
    """Check which academic year we are in"""
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    if month < 9:
        current_year = year - 1
    else:
        current_year = year
    return current_year


class SubjectArea(models.Model):
    """The class representing subject areas.

    A subject area is a broader category, for example "Law" or "Economics".
    Both students and modules can have multiple. A student in a Course like
    "Law with Economics", for example, can be enlisted in modules that list
    "Law" and "Economics" in their subject areas, and a "Law of Corporations"
    module can be open to Law and Economics students. A short title is
    optional ("IR" for "International Relations")."""

    title = models.CharField(max_length=100, unique=True)
    short_title = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.title


class Student(models.Model):
    """The class representing a student"""

    DEGREES = (
        (1, 'First'),
        (21, '2:1'),
        (22, '2:2'),
        (3, 'Third'),
        (4, 'Fail')
    )
    POSSIBLE_YEARS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (7, 'Masters'),
        (8, 'PhD'),
        (9, 'Alumni')
    )

    student_id = models.CharField(
        verbose_name="Student ID",
        max_length=25,
        primary_key=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    exam_id = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Exam ID",
        default=None
    )
    #    belongs_to = models.ForeignKey(
    #        User,
    #        limit_choices_to={'groups__name': 'students'},
    #        blank=True,
    #        null=True
    #    )
    since = models.IntegerField(
        verbose_name="Studying since",
        choices=ACADEMIC_YEARS,
        blank=True,
        null=True
    )
    year = models.IntegerField(choices=POSSIBLE_YEARS, blank=True, null=True)
    is_part_time = models.BooleanField(verbose_name="Part Time", default=False)
    second_part_time_year = models.BooleanField(
        verbose_name="Second part of the year (for part time students only)",
        default=False
    )
    # This box has to be ticked when a part time student is in the second
    # half of a "year": student x might be studying for two years already,
    # but still takes year 1 modules for example
    email = models.CharField(max_length=100, blank=True)
    #    course = models.ForeignKey(Course, blank=True, null=True)
    qld = models.BooleanField(verbose_name="QLD Status", default=True)
    #    tutor = models.ForeignKey(
    #        User,
    #        limit_choices_to={'groups__name': 'teachers'},
    #        blank=True,
    #        null=True,
    #        related_name="tutee"
    #    )
    #    modules = models.ManyToManyField(Module, blank=True)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    lsp = models.TextField(
        verbose_name="Learning Support Plan",
        blank=True,
        null=True
    )
    permanent_email = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, verbose_name="Term Time Address")
    phone_number = models.CharField(max_length=100, blank=True)
    home_address = models.TextField(blank=True)
    nalp = models.BooleanField(
        verbose_name="Paralegal Pathway",
        blank=True,
        default=False,
    )
    tier_4 = models.BooleanField(
        verbose_name="Tier 4 Student",
        blank=True,
        default=False
    )
    achieved_degree = models.IntegerField(
        choices=DEGREES, blank=True, null=True)

    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)

    def get_absolute_url(self):
        return reverse('student_view', args=[self.student_id])

    def get_edit_url(self):
        return reverse('edit_student', args=[self.student_id])


class Module(models.Model):
    """The class representing a module and basic information about assessment.

    The current implementation is limited to 6 assessments per module,
    not counting the exam (where you cannot define a title, wordcount
    or a marksheet.
    """

    ELIGIBLE = (
        ('1', 'Year 1 only'),
        ('2', 'Year 2 only'),
        ('3', 'Year 3 only'),
        ('123', 'All years'),
        ('12', 'Years 1 and 2'),
        ('23', 'Years 2 and 3')
        )  # With these kinds of strings, we can check "if '1' in eligible:"
    CREDITS = (
        (20, '20'),
        (40, '40')
        )
    NO_TEACHING_STR = "No teaching in these weeks (reading weeks, cancelled "
    NO_TEACHING_STR += "seminars etc, separated by a comma)"

    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    #    instructors = models.ManyToManyField(
    #        User,
    #        limit_choices_to={'groups__name': 'teachers'},
    #        blank=True,
    #        null=True
    #        )
    year = models.IntegerField(
        choices=ACADEMIC_YEARS,
        default=this_year()
    )
    # successor_of = models.ForeignKey('self', blank=True, null=True)
    foundational = models.BooleanField(
        verbose_name="Foundational Module",
        default=False
    )
    nalp = models.BooleanField(
        verbose_name="Module is required for the NALP Qualification",
        default=False
    )
    credits = models.IntegerField(default=20, choices=CREDITS)
    eligible = models.CharField(
        max_length=3,
        choices=ELIGIBLE,
        default='1',
        verbose_name="Which students can (or have to) take this module?"
        )
    first_session = models.IntegerField(
        default=5,
        verbose_name="Week of first seminar",
        choices=TEACHING_WEEKS
        )
    no_teaching_in = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=(NO_TEACHING_STR)
    )
    last_session = models.IntegerField(
        default=15,
        verbose_name="Week of last seminar",
        choices=TEACHING_WEEKS
    )
    sessions_recorded = models.IntegerField(blank=True, null=True, default=0)
    # Assessment 1
    assessment_1_title = models.CharField(
        max_length=100,
        verbose_name="Title",
        blank=True,
        null=True
    )
    assessment_1_value = models.IntegerField(
        verbose_name="Value",
        blank=True,
        null=True,
    )
    assessment_1_submission_date = models.DateField(
        verbose_name="Submission Date",
        blank=True,
        null=True
    )
    assessment_1_max_word_count = models.IntegerField(
        verbose_name="Word Count",
        blank=True,
        null=True
    )
    #    assessment_1_marksheet_type = models.CharField(
    #        max_length=50,
    #        verbose_name="Marksheet Type",
    #        blank=True,
    #        null=True,
    #        choices=AVAILABLE_MARKSHEETS
    #        )
    assessment_1_available = models.BooleanField(
        verbose_name="Students can see the mark/feedback",
        default=False
    )
    # Assessment 2
    assessment_2_title = models.CharField(
        max_length=100,
        verbose_name="Title",
        blank=True,
        null=True
    )
    assessment_2_value = models.IntegerField(
        verbose_name="Value",
        blank=True,
        null=True,
    )
    assessment_2_submission_date = models.DateField(
        verbose_name="Submission Date",
        blank=True,
        null=True
    )
    assessment_2_max_word_count = models.IntegerField(
        verbose_name="Word Count",
        blank=True,
        null=True
    )
    #    assessment_2_marksheet_type = models.CharField(
    #        max_length=50,
    #        verbose_name="Marksheet Type",
    #        blank=True,
    #        null=True,
    #        choices=AVAILABLE_MARKSHEETS
    #        )
    assessment_2_available = models.BooleanField(
        verbose_name="Students can see the mark/feedback",
        default=False
    )
    # Assessment 3
    assessment_3_title = models.CharField(
        max_length=100,
        verbose_name="Title",
        blank=True,
        null=True
    )
    assessment_3_value = models.IntegerField(
        verbose_name="Value",
        blank=True,
        null=True,
    )
    assessment_3_submission_date = models.DateField(
        verbose_name="Submission Date",
        blank=True,
        null=True
    )
    assessment_3_max_word_count = models.IntegerField(
        verbose_name="Word Count",
        blank=True,
        null=True
    )
    #    assessment_3_marksheet_type = models.CharField(
    #        max_length=50,
    #        verbose_name="Marksheet Type",
    #        blank=True,
    #        null=True,
    #        choices=AVAILABLE_MARKSHEETS
    #        )
    assessment_3_available = models.BooleanField(
        verbose_name="Students can see the mark/feedback",
        default=False
    )
    # Assessment 4
    assessment_4_title = models.CharField(
        max_length=100,
        verbose_name="Title",
        blank=True,
        null=True
    )
    assessment_4_value = models.IntegerField(
        verbose_name="Value",
        blank=True,
        null=True,
    )
    assessment_4_submission_date = models.DateField(
        verbose_name="Submission Date",
        blank=True,
        null=True
    )
    assessment_4_max_word_count = models.IntegerField(
        verbose_name="Word Count",
        blank=True,
        null=True
    )
    #    assessment_4_marksheet_type = models.CharField(
    #        max_length=50,
    #        verbose_name="Marksheet Type",
    #        blank=True,
    #        null=True,
    #        choices=AVAILABLE_MARKSHEETS
    #        )
    assessment_4_available = models.BooleanField(
        verbose_name="Students can see the mark/feedback",
        default=False
    )
    # Assessment 5
    assessment_5_title = models.CharField(
        max_length=100,
        verbose_name="Title",
        blank=True,
        null=True
    )
    assessment_5_value = models.IntegerField(
        verbose_name="Value",
        blank=True,
        null=True,
    )
    assessment_5_submission_date = models.DateField(
        verbose_name="Submission Date",
        blank=True,
        null=True
    )
    assessment_5_max_word_count = models.IntegerField(
        verbose_name="Word Count",
        blank=True,
        null=True
    )
    #    assessment_5_marksheet_type = models.CharField(
    #        max_length=50,
    #        verbose_name="Marksheet Type",
    #        blank=True,
    #        null=True,
    #        choices=AVAILABLE_MARKSHEETS
    #        )
    assessment_5_available = models.BooleanField(
        verbose_name="Students can see the mark/feedback",
        default=False
    )
    # Assessment 6
    assessment_6_title = models.CharField(
        max_length=100,
        verbose_name="Title",
        blank=True,
        null=True
    )
    assessment_6_value = models.IntegerField(
        verbose_name="Value",
        blank=True,
        null=True,
    )
    assessment_6_submission_date = models.DateField(
        verbose_name="Submission Date",
        blank=True,
        null=True
    )
    assessment_6_max_word_count = models.IntegerField(
        verbose_name="Word Count",
        blank=True,
        null=True
    )
    #    assessment_6_marksheet_type = models.CharField(
    #        max_length=50,
    #        verbose_name="Marksheet Type",
    #        blank=True,
    #        null=True,
    #        choices=AVAILABLE_MARKSHEETS
    #        )
    assessment_6_available = models.BooleanField(
        verbose_name="Students can see the mark/feedback",
        default=False
    )
    # Exam
    exam_value = models.IntegerField(
        verbose_name="Percentage value for the exam",
        default=60,
        blank=True,
        null=True
        )
    exam_available = models.BooleanField(
        verbose_name="Students can see the exam mark",
        blank=True,
        default=False
        )

    class Meta:
        unique_together = ('code', 'year')

    def __unicode__(self):
        next_year = str(int(self.year) + 1)
        nxt = next_year[-2:]
        return u'%s (%s/%s)' % (self.title, self.year, nxt)

    def get_absolute_url(self):
        return reverse('module_view', args=[self.code, self.year])

    def get_edit_url(self):
        return reverse('edit_module', args=[self.code, self.year])
