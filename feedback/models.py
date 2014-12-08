from django.db import models
from main.models import Assessment, AssessmentResult, Staff

class IndividualFeedback(models.Model):
    """The model for a marksheet for an individual performance.

    Make sure to implement setting complete = True in the functions,
    otherwise there will be a warning sign next to the download
    icon in the module view.
    """
    MARKS = (
        (29, '0 - 39 %'),
        (39, '30 - 39 %'),
        (49, '40 - 49 %'),
        (59, '50 - 59 %'),
        (69, '60 - 69 %'),
        (79, '70 - 79 %'),
        (80, '80 or more')
    )
    ATTEMPTS = (
        ('first', 'First Attempt'),
        ('resit', 'First Resit'),
        ('second_resit', 'Second Resit'),
        ('qld_resit', 'QLD Resit')
    )
    assessment_result = models.ForeignKey(
        AssessmentResult, related_name="feedback")
    attempt = models.CharField(max_length=15, choices=ATTEMPTS)
    completed = models.BooleanField(blank=True, default=False)
    markers = models.ManyToManyField(
        Staff,
        blank=True,
        null=True,
        related_name="feedback"
    )
    second_marker = models.ForeignKey(
        Staff,
        blank=True,
        null=True,
        related_name="feedback_as_second_marker"
    )
    marking_date = models.DateField(blank=True, null=True)
    category_mark_1 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_2 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_3 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_4 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_5 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_6 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_7 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_8 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_1_free = models.IntegerField(blank=True, null=True)
    category_mark_2_free = models.IntegerField(blank=True, null=True)
    category_mark_3_free = models.IntegerField(blank=True, null=True)
    category_mark_4_free = models.IntegerField(blank=True, null=True)
    category_mark_5_free = models.IntegerField(blank=True, null=True)
    category_mark_6_free = models.IntegerField(blank=True, null=True)
    category_mark_7_free = models.IntegerField(blank=True, null=True)
    category_mark_8_free = models.IntegerField(blank=True, null=True)
    deduction = models.IntegerField(blank=True, null=True)
    deduction_explanation = models.TextField(blank=True)
    part_1_mark = models.IntegerField(blank=True, null=True)
    part_2_mark = models.IntegerField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True)
    comments_2 = models.TextField(blank=True)

    class Meta:
        unique_together = ('assessment_result', 'attempt')

    def category_mark(self, number, free=False):
        if number == 1:
            if free:
                return self.category_mark_1_free
            else:
                return self.category_mark_1
        if number == 2:
            if free:
                return self.category_mark_2_free
            else:
                return self.category_mark_2
        if number == 3:
            if free:
                return self.category_mark_3_free
            else:
                return self.category_mark_3
        if number == 4:
            if free:
                return self.category_mark_4_free
            else:
                return self.category_mark_4
        if number == 5:
            if free:
                return self.category_mark_5_free
            else:
                return self.category_mark_5
        if number == 6:
            if free:
                return self.category_mark_6_free
            else:
                return self.category_mark_6
        if number == 7:
            if free:
                return self.category_mark_7_free
            else:
                return self.category_mark_7
        if number == 8:
            if free:
                return self.category_mark_8_free
            else:
                return self.category_mark_8


class GroupFeedback(models.Model):
    """The model for a marksheet for a Group Assessment."""
    MARKS = (
        (29, '0 - 39 %'),
        (39, '30 - 39 %'),
        (49, '40 - 49 %'),
        (59, '50 - 59 %'),
        (69, '60 - 69 %'),
        (79, '70 - 79 %'),
        (80, '80 or more')
    )
    ATTEMPTS = (
        ('first', 'First Attempt'),
        ('resit', 'First Resit'),
        ('second_resit', 'Second Resit'),
        ('qld_resit', 'QLD Resit')
    )
    assessment = models.ManyToManyField(
        Assessment, related_name='group_component_feedback')
    group_no = models.IntegerField()
    attempt = models.CharField(max_length=15, choices=ATTEMPTS)
    completed = models.BooleanField(blank=True, default=False)
    marking_date = models.DateField(blank=True, null=True)
    category_mark_1 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_2 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_3 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_4 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_5 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_6 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_7 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_8 = models.IntegerField(choices=MARKS, blank=True, null=True)
    category_mark_1_free = models.IntegerField(blank=True, null=True)
    category_mark_2_free = models.IntegerField(blank=True, null=True)
    category_mark_3_free = models.IntegerField(blank=True, null=True)
    category_mark_4_free = models.IntegerField(blank=True, null=True)
    category_mark_5_free = models.IntegerField(blank=True, null=True)
    category_mark_6_free = models.IntegerField(blank=True, null=True)
    category_mark_7_free = models.IntegerField(blank=True, null=True)
    category_mark_8_free = models.IntegerField(blank=True, null=True)
    individual_mark_1 = models.TextField(blank=True, null=True)
    individual_mark_2 = models.TextField(blank=True, null=True)
    individual_mark_3 = models.TextField(blank=True, null=True)
    individual_mark_4 = models.TextField(blank=True, null=True)
    individual_mark_5 = models.TextField(blank=True, null=True)
    individual_mark_6 = models.TextField(blank=True, null=True)
    individual_mark_7 = models.TextField(blank=True, null=True)
    individual_mark_8 = models.TextField(blank=True, null=True)
    deduction = models.IntegerField(blank=True, null=True)
    deduction_explanation = models.TextField(blank=True)
    part_1_mark = models.IntegerField(blank=True, null=True)
    part_2_mark = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True)
    individual_comments = models.TextField(blank=True)

    def get_group_mark(self, number, free=False):
        if number == 1:
            if free:
                return self.category_mark_1_free
            else:
                return self.category_mark_1
        elif number == 2:
            if free:
                return self.category_mark_2_free
            else:
                return self.category_mark_2
        elif number == 3:
            if free:
                return self.category_mark_3_free
            else:
                return self.category_mark_3
        elif number == 4:
            if free:
                return self.category_mark_4_free
            else:
                return self.category_mark_4
        elif number == 5:
            if free:
                return self.category_mark_5_free
            else:
                return self.category_mark_5
        elif number == 6:
            if free:
                return self.category_mark_6_free
            else:
                return self.category_mark_6
        elif number == 7:
            if free:
                return self.category_mark_7_free
            else:
                return self.category_mark_7
        elif number == 8:
            if free:
                return self.category_mark_8_free
            else:
                return self.category_mark_8

    def get_individual_mark(self, number, student_id):
        if number == 1:
            all_marks = self.individual_mark_1
        elif number == 2:
            all_marks = self.individual_mark_2
        elif number == 3:
            all_marks = self.individual_mark_3
        elif number == 4:
            all_marks = self.individual_mark_4
        elif number == 5:
            all_marks = self.individual_mark_5
        elif number == 6:
            all_marks = self.individual_mark_6
        elif number == 7:
            all_marks = self.individual_mark_7
        elif number == 8:
            all_marks = self.individual_mark_8
        mark_dict = {}
        marks = all.split('\\\///')
        for mark in marks:
            mark_list = mark.split('||:||')
            mark_dict[mark_list[0]] = mark_list[1]
        if student_id in mark_dict:
            return mark_dict[student_id]
        else:
            return None

    def set_individual_mark(self, number, student_id, mark):
        if number == 1:
            all_marks = self.individual_mark_1
        elif number == 2:
            all_marks = self.individual_mark_2
        elif number == 3:
            all_marks = self.individual_mark_3
        elif number == 4:
            all_marks = self.individual_mark_4
        elif number == 5:
            all_marks = self.individual_mark_5
        elif number == 6:
            all_marks = self.individual_mark_6
        elif number == 7:
            all_marks = self.individual_mark_7
        elif number == 8:
            all_marks = self.individual_mark_8
        mark_dict = {}
        marks = all.split('\\\///')
        for mark in marks:
            mark_list = mark.split('||:||')
            mark_dict[mark_list[0]] = mark_list[1]
        mark_dict[student_id] = mark
        string_to_save = ''
        for key, value in mark_dict.items:
            this_string = key + '||::||' + value
            string_to_save += this_string
            string_to_save += '\\\///'
        if number == 1:
            self.individual_mark_1 = string_to_save
        elif number == 2:
            self.individual_mark_2 = string_to_save
        elif number == 3:
            self.individual_mark_3 = string_to_save
        elif number == 4:
            self.individual_mark_4 = string_to_save
        elif number == 5:
            self.individual_mark_5 = string_to_save
        elif number == 6:
            self.individual_mark_6 = string_to_save
        elif number == 7:
            self.individual_mark_7 = string_to_save
        elif number == 8:
            self.individual_mark_8 = string_to_save
        self.save()

    def set_multiple_individual_marks(self, number, set_mark_dict):
        if number == 1:
            all_marks = self.individual_mark_1
        elif number == 2:
            all_marks = self.individual_mark_2
        elif number == 3:
            all_marks = self.individual_mark_3
        elif number == 4:
            all_marks = self.individual_mark_4
        elif number == 5:
            all_marks = self.individual_mark_5
        elif number == 6:
            all_marks = self.individual_mark_6
        elif number == 7:
            all_marks = self.individual_mark_7
        elif number == 8:
            all_marks = self.individual_mark_8
        mark_dict = {}
        marks = all.split('\\\///')
        for mark in marks:
            mark_list = mark.split('||:||')
            mark_dict[mark_list[0]] = mark_list[1]
        for key, value in set_mark_dict.items:
            mark_dict[key] = value
        string_to_save = ''
        for key, value in mark_dict.items:
            this_string = key + '||::||' + value
            string_to_save += this_string
            string_to_save += '\\\///'
        if number == 1:
            self.individual_mark_1 = string_to_save
        elif number == 2:
            self.individual_mark_2 = string_to_save
        elif number == 3:
            self.individual_mark_3 = string_to_save
        elif number == 4:
            self.individual_mark_4 = string_to_save
        elif number == 5:
            self.individual_mark_5 = string_to_save
        elif number == 6:
            self.individual_mark_6 = string_to_save
        elif number == 7:
            self.individual_mark_7 = string_to_save
        elif number == 8:
            self.individual_mark_8 = string_to_save
        self.save()
