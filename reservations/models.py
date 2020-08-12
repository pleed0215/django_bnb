import datetime

from django.db import models
from core.models import AbstractTimeStamped
from django.utils import timezone


class BookedDay(AbstractTimeStamped):
    day = models.DateField(null=True)
    reservation = models.ForeignKey(
        "reservations.Reservation",
        related_name="my_booked_days",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.day)


# Create your models here.
class Reservation(AbstractTimeStamped):
    """ Reservation model definition """

    STATUS_PENDING = "pending"
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

    checkin_date = models.DateField(null=True)
    checkout_date = models.DateField(null=True)

    # foreign key
    guest = models.ForeignKey(
        "users.User", related_name="my_reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="my_reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Room: {self.room} reservation on {self.checkin_date}"

    def is_in_progress(self):
        today = timezone.now().date()
        return (today >= self.checkin_date) and (today <= self.checkout_date)

    is_in_progress.short_description = "progress?"
    is_in_progress.boolean = True

    def is_finished(self):
        today = timezone.now().date()
        return today > self.checkout_date

    is_finished.short_description = "finished?"
    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:
            start = self.checkin_date
            end = self.checkout_date
            difference = end - start

            is_reservated = BookedDay.objects.filter(day__range=(start, end)).exists()
            if is_reservated is False:
                super().save(*args, **kwargs)

                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)

        else:

            return super().save(*args, **kwargs)

