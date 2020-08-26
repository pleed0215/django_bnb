from django.db import models
from django.contrib.auth.models import UserManager


class CustomReservationManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return super().get(**kwargs)
        except self.model.DoesNotExist:
            return None


class CustomuserManager (UserManager, CustomReservationManager):
    pass
