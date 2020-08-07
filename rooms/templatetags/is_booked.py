import datetime
from django import template
from reservations.models import BookedDay

register = template.Library()


@register.simple_tag
def is_booked(room, day):
    if day.day == 0:
        return
    try:
        date = datetime.datetime(day.year, day.month, day.day)
        BookedDay.objects.get(day=date, reservation__room=room)

        return True
    except BookedDay.DoesNotExist:

        return False
