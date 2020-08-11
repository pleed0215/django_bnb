import datetime
from django.shortcuts import render
from django.shortcuts import redirect, reverse
from .models import BookedDay, Reservation
from rooms.models import Room
from django.contrib import messages
from django.views.generic import View
from django.http import Http404


class AlreadyReserved(Exception):
    pass

# Create your views here.
def create(request, room, year, month, day):
    try:
        reserved_date = datetime.datetime(year, month, day)
        room = Room.objects.get(pk=room)
        booked = BookedDay.objects.get(day=reserved_date, reservation__room = room)
        # booked need not to be exist for reservation.
        raise AlreadyReserved()
    except (Room.DoesNotExist, AlreadyReserved):
        messages.error (request, "Invalid access for making a reservation.")
        return redirect(reverse("core:home"))
    except BookedDay.DoesNotExist:
        reservation = Reservation.objects.create (
            checkin_date=reserved_date,
            checkout_date=reserved_date + datetime.timedelta(days=1),
            room = room,
            guest=request.user,
        )
        return redirect(reverse("reservations:detail", kwargs={"pk":reservation.pk}))

"""class ReservationDetailView(DetailView):
    model = Reservation"""
class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = Reservation.objects.get_or_none (pk=pk)

        if reservation is None:
            raise Http404("Invalid access")

        print (reservation.guest != self.request.user)
        print (reservation.room.host != self.request.user)
        if reservation.guest != self.request.user and reservation.room.host != self.request.user:
            raise Http404("Neither guest or host.")

        return render(self.request, "reservations/reservation_detail.html", {"object": reservation})
        
