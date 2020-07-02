from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """ reservation admin page definition """

    list_display = (
        "room",
        "guest",
        "status",
        "checkin_date",
        "checkout_date",
        "is_in_progress",
        "is_finished",
    )

    list_filter = ("status",)

