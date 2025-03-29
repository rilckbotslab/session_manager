""" This file contains the models for the database. """


from django.db import models
from .manage import init_django

init_django()

class YudqsLogs(models.Model):
    id = models.AutoField(primary_key=True)
    log_datetime = models.DateTimeField(null=False)
    requisition_id = models.CharField(max_length=50)
    sdc_id = models.CharField(max_length=50)
    buyer_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    unit = models.CharField(max_length=150)
    type = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    baseline_value = models.FloatField()
    log_message = models.TextField()
    process_information = models.TextField()
    process_message = models.TextField()
    processed = models.IntegerField()

    class Meta:
        db_table = 'yduqs_logs'
