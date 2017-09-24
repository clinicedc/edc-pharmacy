from django.db import models


class DispenseSchedule(models.Model):

    name = models.CharField(max_length=100,)

    sequence = models.IntegerField()

    duration = models.CharField(max_length=100,)

    start_date = models.DateField()

    end_date = models.DateField()

    class Meta:
        app_label = 'edc_pharma'


class DispenseryPlan(models.Model):

    subject_identifier = models.CharField(
        max_length=150,)

    timepoint = models.DateField()

    schedule = models.ForeignKey(DispenseSchedule)

    class Meta:
        app_label = 'edc_pharma'
