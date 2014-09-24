from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from feedback.categories import AVAILABLE_MARKSHEETS
from main.unisettings import TEACHING_WEEKS
import datetime

ACADEMIC_YEARS = (
    [(i, str(i) + "/" + str(i+1)[-2:]) for i in range(2010, 2025)]
)


def this_year():
    """Checks which academic year we are in"""
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    if month < 9:
        current_year = year - 1
    else:
        current_year = year
    return current_year


class Setting(models.Model):
    """Allows to save some general settings in the database"""
    name = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=200)


class Data(models.Model):
    """Allows to save some data for passing it between functions

    A management function set by a Cron job will delete data instances
    older than 14 days to save space.
    """
    id = models.CharField(max_length=20, primary_key=True)
    value = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)


class SubjectArea(models.Model):
    """Subject areas are the broader categories - eg "Law" or "Economics".

    Both students and modules can have multiple. A student in a Course like
    "Law with Economics", for example, can be enlisted in modules that list
    "Law" and "Economics" in their subject areas, and a "Law of Corporations"
    module can be open to Law and Economics students. A short title is
    optional ("IR" for "International Relations").
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Add...")
    slug = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubjectArea, self).save(*args, **kwargs)


class Course(models.Model):
    """Courses are the programmes of students - eg "Law with Economics" """
    title = models.CharField(max_length=100, unique=True)
    short_title = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True
    )
    subject_areas = models.ManyToManyField(
        SubjectArea, blank=True, related_name='courses')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_overview')

    def get_edit_url(self):
        return reverse('edit_course', args=[self.id])


class Staff(models.Model):
    """The class representing a teacher with additional information"""
    ROLES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
    )

    user = models.OneToOneField(User)
    subject_areas = models.ManyToManyField(SubjectArea, blank=True, null=True)
    role = models.CharField(
        choices=ROLES, max_length=10, default='teacher')
    pastoral_care = models.BooleanField(default=False)
    programme_director = models.BooleanField(default=False)
    main_admin = models.BooleanField(default=False)  # Sees all subjects

    class Meta:
        ordering = ['user']

    def __str__(self):
        subject_list = []
        for subject in self.subject_areas.all():
            subject_list.append(subject.name)
        subjects = '/'.join(subject_list)
        return "%s %s (%s)" % (
            self.user.first_name, self.user.last_name, subjects)

    def name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def get_edit_url(self):
        return reverse('edit_staff', args=[self.user.username])

    def get_delete_url(self):
        return reverse('delete_staff_member', args=[self.user.username])


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
        ('7', 'Masters Students only'),
        ('8', 'PhD Students only'),
        ('123', 'All years'),
        ('12', 'Years 1 and 2'),
        ('23', 'Years 2 and 3')
    )  # With these kinds of strings, we can check "if '1' in eligible:"
    CREDITS = (
        (10, '10'),
        (20, '20'),
        (30, '20'),
        (40, '40')
    )
    NO_TEACHING_STR = "No teaching in these weeks (reading weeks, cancelled "
    NO_TEACHING_STR += "seminars etc, separated by a comma)"

    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    year = models.IntegerField(
        choices=ACADEMIC_YEARS,
        default=this_year()
    )
    subject_areas = models.ManyToManyField(
        SubjectArea,
        verbose_name='Open for'
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
        verbose_name="Which students can (or have to) take this module?",
        blank=True,
        null=True
        )
    first_session = models.IntegerField(
        default=5,
        verbose_name="Week of first seminar",
        choices=TEACHING_WEEKS,
        blank=True,
        null=True
        )
    no_teaching_in = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=(NO_TEACHING_STR),
        null=True
    )
    last_session = models.IntegerField(
        default=15,
        verbose_name="Week of last seminar",
        choices=TEACHING_WEEKS,
        blank=True,
        null=True
    )
    teachers = models.ManyToManyField(
        Staff, limit_choices_to={'role': 'teacher'}, related_name='modules'
    )

    class Meta:
        unique_together = ('code', 'year')

    def __str__(self):
        next_year = str(int(self.year) + 1)
        nxt = next_year[-2:]
        return u'%s (%s/%s)' % (self.title, self.year, nxt)

    def get_absolute_url(self):
        return reverse('module_view', args=[self.code, self.year])

    def link(self):
        link = (
            '<a href="' +
            self.get_absolute_url() +
            '">' +
            self.title +
            '</a>'
        )
        return link

    def get_edit_url(self):
        return reverse('edit_module', args=[self.code, self.year])

    def get_add_students_url(self):
        return reverse('add_students_to_module', args=[self.code, self.year])

    def get_attendance_url(self, group):
        group = str(group)
        return reverse('attendance', args=[self.code, self.year, group])

    def get_export_attendance_sheet_url(self):
        return reverse('export_attendance_sheet', args=[self.code, self.year])

    def get_delete_self_url(self):
        return reverse('delete_module', args=[self.code, self.year])

    def get_seminar_groups_url(self):
        return reverse('assign_seminar_groups', args=[self.code, self.year])

    def get_seminar_group_overview_url(self):
        return reverse('seminar_group_overview', args=[self.code, self.year])

    def get_assessment_url(self):
        return reverse('assessment', args=[self.code, self.year])

    def get_remove_student_url(self, student_id):
        return reverse(
            'remove_student_from_module',
            args=[self.code, self.year, student_id]
        )

    def get_blank_remove_student_url(self):
        url = reverse(
            'remove_student_from_module',
            args=[self.code, self.year, 'xxxxxxxxxxxxxxxxxxxx']
        )
        blank_url = url.replace('xxxxxxxxxxxxxxxxxxxx/', '')
        return blank_url

    def all_assessment_titles(self):
        returnlist = []
        exam = False
        for assessment in self.assessments.all():
            if assessment.title != 'Exam':  # Make sure the exam comes last
                returnlist.append((assessment.title, assessment.value))
            else:
                exam = ('Exam', assessment.value)
        if exam:
            returnlist.append(exam)
        return returnlist

    def all_assessments(self):
        returnlist = []
        exam = False
        for assessment in self.assessments.all():
            if assessment.title != 'Exam':  # Make sure the exam comes last
                returnlist.append(assessment)
            else:
                exam = assessment
        if exam:
            returnlist.append(exam)
        return returnlist

    def all_teaching_weeks(self):
        no_teaching = []
        if self.no_teaching_in:
            if ',' in self.no_teaching_in:
                no_teaching_strings = self.no_teaching_in.split(',')
            else:
                no_teaching_strings = [self.no_teaching_in]
            for entry in no_teaching_strings:
                try:
                    no_teaching.append(int(entry))
                except ValueError:
                    pass
        returnlist = []
        last = self.last_session + 1
        for week in range(self.first_session, last):
            if week not in no_teaching:
                returnlist.append(week)
        returnlist.sort()
        return returnlist


class Assessment(models.Model):
    """The basic information about an assessment"""
    module = models.ForeignKey(
        Module,
        related_name='assessments',
        blank=True,
        null=True
    )
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True, null=True)
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
    group_assessment = models.BooleanField(default=False)
    marksheet_type = models.CharField(
        max_length=50,
        verbose_name="Marksheet Type",
        blank=True,
        null=True,
        choices=AVAILABLE_MARKSHEETS
    )
    co_marking = models.BooleanField(
        default=False,
        verbose_name=(
            "Co-Marking (all teachers on this module appear on the marksheet)")
    )
    available = models.BooleanField(
        verbose_name="Students can see the mark/feedback",
        default=False
    )

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Assessment, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'edit_assessment',
            args=[self.module.code, self.module.year, self.slug]
        )

    def get_delete_url(self):
        return reverse(
            'delete_assessment',
            args=[self.module.code, self.module.year, self.slug]
        )


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
    user = models.OneToOneField(User, blank=True, null=True)
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
    tutor = models.ForeignKey(
        Staff,
        blank=True,
        null=True,
        related_name="tutees"
    )
    modules = models.ManyToManyField(
        Module, blank=True, related_name="students")
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    lsp = models.TextField(
        verbose_name="Learning Support Plan",
        blank=True,
        null=True
    )
    permanent_email = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, verbose_name="Term Time Address")
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    cell_number = models.CharField(max_length=50, blank=True, null=True)
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
    tutor = models.ForeignKey(
        Staff,
        blank=True,
        null=True,
        related_name="tutees"
    )

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)

    def short_first_name(self):
        first_names = self.first_name.split(" ")
        return first_names[0]

    def short_name(self):
        return "%s, %s" % (self.last_name, self.short_first_name())

    def name(self):
        return "%s %s" % (self.short_first_name(), self.last_name)

    def get_absolute_url(self):
        return reverse('student_view', args=[self.student_id])

    def get_link(self):
        html = (
            '<a href="' +
            self.get_absolute_url() +
            '">' +
            self.short_name() +
            '</a>'
        )
        return html

    def get_edit_url(self):
        return reverse('edit_student', args=[self.student_id])

    def html_address(self):
        address = self.address.replace("\n", "<br>")
        return address

    def html_home_address(self):
        address = self.home_address.replace("\n", "<br>")
        return address


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
    qld_resit = models.IntegerField(blank=True, null=True)
    marksheet_done = models.BooleanField(default=False)

    class Meta:
        ordering = ['assessment']

    def result_as_string(self):
        if self.mark is None:
            returnstring = None
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
                if self.second_resit_mark:
                    if self.second_concessions == self.GRANTED:
                        if self.assessment.title == 'Exam':
                            resit_type = 'Sit'
                        else:
                            resit_type = 'Submission'
                    else:
                        if self.assessment.title == 'Exam':
                            resit_type = 'Resit'
                        else:
                            resit_type = 'Resubmission'
                    returnstring += ", Second %s: %s" % (
                        resit_type, self.second_resit_mark)
                elif self.qld_resit:
                    returnstring += (
                        ", QLD Resit: %s" % (self.qld_resit)
                    )
                returnstring += ")"
        return returnstring

    def module_needs_to_be_capped(self):
        cap = False
        if self.resit_mark:
            if self.concessions in [self.NO_CONCESSIONS, self.PENDING]:
                cap = True
        if self.second_resit_mark:
            if self.second_concessions in [self.NO_CONCESSIONS, self.PENDING]:
                cap = True
        return cap

    def result(self):
        result = self.mark
        if self.resit_mark:
            if self.resit_mark > result:
                result = self.resit_mark
            if self.second_resit_mark:
                if self.second_resit_mark > result:
                    result = self.second_resit_mark
        return result

    def no_qld_problems(self):
        if self.mark:
            if self.mark > 40:
                return True
            elif self.resit_mark and self.resit_mark > 40:
                return True
            else:
                if self.second_resit_mark:
                    if self.second_resit_mark > 40:
                        return True
                elif self.qld_resit:
                    if self.qld_resit > 40:
                        return True
        return False


class Performance(models.Model):
    """The Performance class connects a student with a module"""
    ATTENDANCE_ENTRIES = (
        ('p', 'Present'),
        ('a', 'Absent'),
        ('e', 'Excused Absence')
    )

    student = models.ForeignKey(Student, related_name="performances")
    module = models.ForeignKey(Module, related_name="performances")
    seminar_group = models.IntegerField(blank=True, null=True)
    belongs_to_year = models.IntegerField(blank=True, null=True)
    assessment_results = models.ManyToManyField(
        AssessmentResult, related_name="part_of")
    # Average
    average = models.IntegerField(blank=True, null=True)  # For display
    real_average = models.FloatField(blank=True, null=True)  # For calculation
    # Attendance: week:string/week/string...
    attendance = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'module')
        ordering = ['module', 'student']

    def all_assessment_results_as_strings(self):
        return_list = []
        there_is_an_exam = False
        all_results = {}
        for result in self.assessment_results.all():
            all_results[result.assessment] = result
        for assessment in self.module.all_assessments():
            if assessment.title != 'Exam':
                if assessment in all_results:
                    result = all_results[assessment]
                    return_list.append(result.result_as_string())
                else:
                    return_list.append(None)
            else:
                there_is_an_exam = True
                if assessment in all_results:
                    result = all_results[assessment]
                    exam = result.result_as_string()
                else:
                    exam = None
        if there_is_an_exam:
            return_list.append(exam)
        return return_list

    def all_assessment_results_as_tpls(self, only_result=False):
        return_list = []
        there_is_an_exam = False
        all_results = {}
        for result in self.assessment_results.all():
            all_results[result.assessment] = result
        for assessment in self.module.all_assessments():
            if assessment.title != 'Exam':
                if assessment in all_results:
                    result = all_results[assessment]
                    if only_result:
                        return_tpl = (assessment.title, result.result())
                    else:
                        return_tpl = (
                            assessment.title, result.result_as_string())
                    return_list.append(return_tpl)
                else:
                    return_list.append((assessment.title, None))
            else:
                there_is_an_exam = True
                if assessment in all_results:
                    result = all_results[assessment]
                    if only_result:
                        exam = result.result()
                    else:
                        exam = result.result_as_string()
                else:
                    exam = None
        if there_is_an_exam:
            return_list.append(('Exam', exam))
        if not only_result:
            return_list.append(('<strong>Result</strong>', self.average))
        return return_list

    def calculate_average(self):
        sum_of_marks = 0
        for assessment in self.module.assessments.all():
            try:
                assessment_result = AssessmentResult.objects.get(
                    assessment=assessment, part_of=self)
                this = assessment_result.result() * assessment.value
                sum_of_marks += this
            except AssessmentResult.DoesNotExist:
                pass
        average = sum_of_marks / 100
        self.real_average = average
        self.average = round(average)
        self.save()

    def set_assessment_result(self, assessment_slug, mark, attempt='first'):
        assessment = Assessment.objects.get(
            module=self.module,
            slug=assessment_slug
        )
        if self.assessment_results.filter(assessment=assessment).exists():
            assessment_result = self.assessment_results.get(
                assessment=assessment)
        else:
            assessment_result = AssessmentResult.objects.create(
                assessment=assessment)
            self.assessment_results.add(assessment_result)
        if attempt == 'first':
            assessment_result.mark = int(mark)
        elif attempt == 'resit':
            assessment_result.resit_mark = int(mark)
        elif attempt == 'second_resit':
            assessment_result.second_resit_mark = int(mark)
        elif attempt == 'qld_resit':
            assessment_result.qld_resit = int(mark)
        assessment_result.save()
        self.calculate_average()

    def get_assessment_result(self, assessment_slug, attempt='all'):
        assessment = Assessment.objects.get(
            module=self.module,
            slug=assessment_slug
        )
        if self.assessment_results.filter(assessment=assessment).exists():
            assessment_result = self.assessment_results.get(
                assessment=assessment)
        else:
            return None
        if attempt == 'all':
            return assessment_result.result()
        elif attempt == 'string':
            return assessment_result.result_as_string()
        elif attempt == 'first':
            return assessment_result.mark
        elif attempt == 'resit':
            return assessment_result.resit_mark
        elif attempt == 'second_resit':
            return assessment_result.second_resit_mark
        elif attempt == 'qld_resit':
            return assessment_result.qld_resit

    def attendance_as_dict(self):
        return_dict = {}
        if self.attendance:
            if '/' in self.attendance:
                p_list = self.attendance.split('/')
                for entry in p_list:
                    entry_list = entry.split(':')
                    return_dict[entry_list[0]] = entry_list[1]
            else:
                if ':' in self.attendance:
                    entry = self.attendance.split(':')
                    return_dict[entry[0]] = entry[1]
        return return_dict

    def attendance_for(self, week):
        week = str(week)
        attendance = self.attendance_as_dict()
        if week in attendance:
            return attendance[week]
        else:
            return None

    def save_attendance(self, week, presence):
        week = str(week)
        attendance = self.attendance_as_dict()
        attendance[week] = presence
        attendance_string = ''
        first_run = True
        for week_no in attendance:
            if not first_run:
                attendance_string += '/'
            else:
                first_run = False
            attendance_string += week_no
            attendance_string += ':'
            attendance_string += attendance[week_no]
        self.attendance = attendance_string
        self.save()

    def count_attendance(self):
        attendance = self.attendance_as_dict()
        present = 0
        absent = 0
        for week, presence in attendance.items():
            if presence in ['p', 'e']:
                present += 1
            elif presence == 'a':
                absent += 1
        returnstring = str(present) + "/" + str(present + absent)
        return returnstring

    def attendance_as_list(self):
        attendance = self.attendance_as_dict()
        returnlist = []
        weeklist = []
        for week in attendance:
            weeklist.append(int(week))  # Otherwise 10 will be before 2!
        weeklist.sort()
        for week in weeklist:
            returnlist.append(attendance[str(week)])
        return returnlist

    def missed_the_last_two_sessions(self):
        attendancelist = self.attendance_as_list()
        if len(attendancelist) >= 2:
            if attendancelist[-1] == 'a':
                if attendancelist[-2] == 'a':
                    return True
        return False


class TuteeSession(models.Model):
    tutee = models.ForeignKey(Student)
    tutor = models.ForeignKey(Staff)
    date_of_meet = models.DateField(verbose_name="Date")
    notes = models.TextField()
    meeting_took_place = models.BooleanField(default=True)

    class Meta:
        ordering = ['date_of_meet', 'tutor']

    def get_absolute_url(self):
        tutee_url = reverse(
            'edit_tutee_meeting',
            args=[self.tutee.student_id, self.id]
        )
        tutee_url += "#" + str(self.id)
        return tutee_url

    def get_edit_url(self):
        this_url = reverse(
            'edit_tutee_meeting',
            args=[self.tutee.student_id, self.id]
        )
        this_url += "#" + 'edit'
        return this_url

    def get_delete_url(self):
        return reverse('delete_tutee_meeting', args=[self.id])
