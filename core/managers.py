from django.db import models


class CustomReservationManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return super().get(**kwargs)
        except self.model.DoesNotExist:
            return None
