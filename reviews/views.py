from django.shortcuts import render, redirect, reverse
from .forms import CreateReviewForm
from rooms.models import Room
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


@login_required
def create_review(request, room):
    if request.method == "POST":
        form = CreateReviewForm(request.POST)
        room = Room.objects.get_or_none(pk=room)

        if room is None:
            return redirect("core:home")

        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user

            review.save()

        messages.success(request, "Review created")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))

