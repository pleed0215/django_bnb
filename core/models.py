from django.db import models

# Create your models here.
class AbstractTimeStamped(models.Model):
    """ Time Stamped Model """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True