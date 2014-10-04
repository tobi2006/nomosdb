from django.db import models
from main.models import *

class IndividualFeedback(models.Model):
    """The model for a marksheet for an individual performance.

    Make sure to implement setting complete = True in the functions,
    otherwise there will be a warning sign next to the download
    icon in the module view.
    """
    MARKS = (
        (39, '0 - 39 %'),
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
    assessment_result = models.ForeignKey(AssessmentResult)
    attempt = models.CharField(max_lenght=15, choices=ATTEMPTS)
    completed = models.BooleanField(blank=True, default=False)
    marker = models.ForeignKey(
        Staff,
        blank=True,
        null=True,
        related_name="feedback"
    )
    second_first_marker = models.ForeignKey(
        Staff,
        blank=True,
        null=True,
        related_name="feedback_as_second_first_marker"
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

