from django.db import models

# Create your models here.
from customers.models import CustomUserModel, TimeStampedModel

import random
import datetime

PRIORITY_CHOICES = (
    ('High', 'HIGH'),
    ('Medium', 'MEDIUM'),
    ('Low', 'LOW')
)

PROGRESS_STATUS = (
    ('Open', 'OPEN'),
    ('In progress', 'IN PROGRESS'),
    ('Closed', 'CLOSED')
)

# A model for the incident model


class IncidentModel(TimeStampedModel):

    incident_pk = models.AutoField(
        primary_key=True, unique=True, editable=False)
    fk_user_uuid = models.ForeignKey(
        'customers.CustomUserModel', on_delete=models.PROTECT, null=True, blank=True)
    incident_id = models.CharField(max_length=30)
    incident_details = models.TextField(editable=True)
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=15, choices=PROGRESS_STATUS)
    close_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):

        if self:
            existing_incident_recs_list = [
                i for i in IncidentModel.objects.all().values("incident_id")]

            incident_id_accept_bool = False
            while not incident_id_accept_bool:
                rand_num = str(random.randint(10000, 99999))
                incident_id_trial = 'RMG' + rand_num + \
                    str(datetime.datetime.now().year)

                if incident_id_trial not in existing_incident_recs_list:
                    incident_id_accept_bool = True
                    self.incident_id = incident_id_trial

        super().save(*args, **kwargs)

    # On incident status?

    def incident_status(self):
        return self.status

    # On Priority?
    def incident_priority(self):
        return self.priority

    # incident_id format?
    def __str__(self):
        return str(self.incident_id)

    class Meta:
        abstract = False
        db_table = "Incidents"
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"
