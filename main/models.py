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
    """Subject areas are the broader categories - eg "Law" or "Economics".

    Both students and modules can have multiple. A student in a Course like
    "Law with Economics", for example, can be enlisted in modules that list
    "Law" and "Economics" in their subject areas, and a "Law of Corporations"
    module can be open to Law and Economics students. A short title is
    optional ("IR" for "International Relations")."""

    name = models.CharField(max_length=100, unique=True, verbose_name="Add...")

    def __unicode__(self):
        return self.name


class Course(models.Model):
    """Courses are the programmes of students - eg "Law with Economics" """
    title = models.CharField(max_length=100, unique=True)
    short_title = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True
    )
    subject_areas = models.ManyToManyField(SubjectArea, blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_overview')

    def get_edit_url(self):
        return reverse('edit_course', args=[self.id])


class Assessment(models.Model):
    """The basic information about an assessment"""
    title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )
    value = models.IntegerField(
        verbose_name="Value",
        blank=True,
        null=True,
    )
    submission_date = models.DateField(
        verbose_name="Submission Date",
        blank=True,
        null=True
    )
    max_word_count = models.IntegerField(
        verbose_name="Word Count",
        blank=True,
        null=True
    )
    #    marksheet_type = models.CharField(
    #        max_length=50,
    #        verbose_name="Marksheet Type",
    #        blank=True,
    #        null=True,
    #        choices=AVAILABLE_MARKSHEETS
    #        )
    available = models.BooleanField(
        verbose_name="Students can see the mark/feedback",
        default=False
    )

    class Meta:
        ordering = ['title']
        

class Module(models.Model):
    """Modules are the subjects - eg "Law of Contracts".

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
    subject_areas = models.ManyToManyField(SubjectArea, blank=True)
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
    assessments = models.ManyToManyField(Assessment, blank=True, null=True)

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

    def get_add_students_url(self):
        return reverse('add_students_to_module', args=[self.code, self.year])

    def get_attendance_url(self, group):
        group = str(group)
        return reverse('attendance', args=[self.code, self.year, group])

    def get_seminar_groups_url(self):
        return reverse('assign_seminar_groups', args=[self.code, self.year])

    def all_assessment_titles(self):
        returnlist = []
        exam = False
        for assessment in self.assessments.all():
            if assessment.title != 'Exam': # Make sure the exam comes last
                returnlist.append((assessment.title, assessment.value))
            else:
                exam = ('Exam', assessment.value)
        if exam:
            returnlist.append(exam)
        return returnlist


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
    course = models.ForeignKey(Course, blank=True, null=True)
    qld = models.BooleanField(verbose_name="QLD Status", default=True)
    #    tutor = models.ForeignKey(
    #        User,
    #        limit_choices_to={'groups__name': 'teachers'},
    #        blank=True,
    #        null=True,
    #        related_name="tutee"
    #    )
    modules = models.ManyToManyField(Module, blank=True)
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

    def short_first_name(self):
        first_names = self.first_name.split(" ")
        return first_names[0]

    def short_name(self):
        return "%s, %s" % (self.last_name, self.short_first_name())

    def get_absolute_url(self):
        return reverse('student_view', args=[self.student_id])

    def get_edit_url(self):
        return reverse('edit_student', args=[self.student_id])


class AssessmentResult(models.Model):
    """How a particular student does in an assessment"""
    NO_CONCESSIONS = 'N'
    PENDING = 'P'
    GRANTED = 'G'
    CONCESSIONS = (
        (NO_CONCESSIONS, 'No concession'),
        (PENDING, 'Concession pending'),
        (GRANTED, 'Concession granted')
    )
    assessment = models.ForeignKey(Assessment)
    mark = models.IntegerField(blank=True, null=True)
    resit_mark = models.IntegerField(blank=True, null=True)
    concessions = models.CharField(
        choices=CONCESSIONS,
        max_length=1,
        blank=True,
        null=True,
        default=NO_CONCESSIONS
    )
    second_resit_mark = models.IntegerField(blank=True, null=True)
    second_concessions = models.CharField(
        choices=CONCESSIONS,
        max_length=1,
        blank=True,
        null=True,
        default=NO_CONCESSIONS
    )
    assessment_group = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['assessment']

    def result_as_string(self):
        if self.mark is None:
            returnstring = ''
        else:
            returnstring = str(self.mark)
            if self.resit_mark:
                if self.concessions == self.GRANTED:
                    if self.assessment.title == 'Exam':
                        resit_type = 'Sit'
                    else:
                        resit_type = 'Submission'
                else:
                    if self.assessment.title == 'Exam':
                        resit_type = 'Resit'
                    else:
                        resit_type = 'Resubmission'
                returnstring += " (%s: %s" % (resit_type, self.resit_mark)
                # The following needs to be changed to allow second resits
                if self.second_resit_mark:
                    returnstring += (
                        ", Second resubmission: %s" % (self.second_resit_mark)
                    )
                returnstring += ")"
        return returnstring


    def module_needs_to_be_capped(self):
        if self.resit_mark:
            if self.concessions in [self.NO_CONCESSIONS, self.PENDING]:
                return True
        return False
    

class Performance(models.Model):
    """The Performance class connects a student with a module"""

    student = models.ForeignKey(Student)
    module = models.ForeignKey(Module)
    seminar_group = models.IntegerField(blank=True, null=True)
    student_year = models.IntegerField(blank=True, null=True)
    assessment_results = models.ManyToManyField(
        AssessmentResult,
        blank=True,
        null=True,
        related_name="part_of"
    )
    # Average
    average = models.IntegerField(blank=True, null=True)  # For display
    real_average = models.FloatField(blank=True, null=True)  # For calculation

    class Meta:
        unique_together = ('student', 'module')
        ordering = ['module', 'student']

    
    def all_assessment_results_as_strings(self):
        return_list = []
        exam = False
        for result in self.assessment_results.all():
            if result.assessment.title != 'Exam': # Make sure exam comes last
                return_list.append(result.result_as_string())
            else:
                exam = result.result_as_string()
        if exam:
            return_list.append(exam)
        return return_list
            

    # def safe(self, *args, **kwargs):
    #    marks = 0
    #        cap = False
    #        if self.assessment_1:
    #            if self.r_assessment_1:
    #                if self.r_assessment_1 > self.assessment_1:
    #                    marks =
    #            else:
    #                all += self.assessment_1
    # after: super(Performance, self).save(*args, **kwargs)


class Session(models.Model):
    """Simply a recorded session for attendance purposes"""
    module = models.ForeignKey(Module)
    group = models.IntegerField(blank=True, null=True)
    date = models.DateField()

class Attendance(models.Model):
    """The attendance for one student at one session"""
    ENTRIES = (
        ('p', 'Present'),
        ('a', 'Absent'),
        ('e', 'Excused Absence')
    )
    performance = models.ForeignKey(Performance)
    session = models.ForeignKey(Session)
