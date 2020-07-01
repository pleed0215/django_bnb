from django.db import models
from core.models import AbstractTimeStamped
from django.utils import timezone

# Create your models here.
class Reservation(AbstractTimeStamped):
    """ Reservation model definition """

    STATUS_PENDING = "peding"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"
    STATUS_CHOICE = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICE, default=STATUS_PENDING
    )

    checkin_date = models.DateField(null=True, default=timezone.now())
    checkout_date = models.DateField(null=True, default=timezone.now())

    # foreign key
    guest = models.ForeignKey(
        "users.User", related_name="my_reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="my_reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Room: {self.room} reservation on {self.checkin_date}"
