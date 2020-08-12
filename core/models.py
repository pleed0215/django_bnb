from django.db import models
from . import managers

# Create your models here.
class AbstractTimeStamped(models.Model):
    """ Time Stamped Model """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = managers.CustomReservationManager()

    class Meta:
        abstract = True
