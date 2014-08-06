from django.db import models

DEGREES = (
    (1, 'First'),
    (21, '2:1'),
    (22, '2:2'),
    (3, 'Third'),
    (4, 'Fail')
)
ACADEMIC_YEARS = (
    [(i, str(i) + "/" + str(i+1)) for i in range(2009, 2025)]
)
TEACHING_WEEKS = (
    [(i, 'Week ' + str(i)) for i in range(1, 53)]
)
POSSIBLE_YEARS = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (7, 'Masters'),
    (8, 'PhD'),
    (9, 'Alumni')
)


class Student(models.Model):
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
        default=False
    )
    tier_4 = models.BooleanField(
        verbose_name="Tier 4 Student",
        blank=True,
        default=False
    )
    achieved_degree = models.IntegerField(
        choices=DEGREES, blank=True, null=True)
