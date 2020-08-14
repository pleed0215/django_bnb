from django.shortcuts import render, redirect, reverse
from .models import List
from rooms.models import Room

# Create your views here.


def toggle_list(request, room_pk):
    room = Room.objects.get_or_none(pk=room_pk)
    action = request.GET.get("action", None)

    if room is not None:

        if action == "add":
            fav_list, _ = List.objects.get_or_create(
                user=request.user, name="favorite list")
            fav_list.rooms.add(room)
        elif action == "remove":
            fav_list = List.objects.get_or_none(
                user=request.user, name="favorite list")
            if fav_list is not None:
                fav_list.rooms.remove(room)

    return redirect(reverse("core:home"))
