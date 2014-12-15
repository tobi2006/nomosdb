from django.db import models
from main.models import Assessment, AssessmentResult, Staff

class IndividualFeedback(models.Model):
    """The model for a marksheet for an individual performance.

    Make sure to implement setting completed = True in the functions,
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
    individual_mark = models.IntegerField(blank=True, null=True)
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
    """The model for the group part of a Group Assessment."""
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
    group_number = models.IntegerField()
    attempt = models.CharField(max_length=15, choices=ATTEMPTS)
    assessment = models.ForeignKey(
        Assessment, related_name="group_feedback")
    completed = models.BooleanField(blank=True, default=False)
    group_mark = models.IntegerField(blank=True, null=True)
    markers = models.ManyToManyField(
        Staff,
        blank=True,
        null=True,
        related_name="group_feedback"
    )
    second_marker = models.ForeignKey(
        Staff,
        blank=True,
        null=True,
        related_name="group_feedback_as_second_marker"
    )
    marking_date = models.DateField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
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
    comments = models.TextField(blank=True)

    class Meta:
        unique_together = ('assessment', 'group_number', 'attempt')

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
