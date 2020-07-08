from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


# Create your views here.
def all_rooms(request):
    all_rooms = Room.objects.all()
    # return HttpResponse(content="<h1>Hello</h1>")
    return render(request, "rooms/home.html", context={"rooms": all_rooms},)
