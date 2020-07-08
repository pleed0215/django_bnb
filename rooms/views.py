from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Create your views here.
def all_rooms(request):
    msg = "Hello, this is all rooms of our site!"
    now = datetime.now()
    hungry = False
    # return HttpResponse(content="<h1>Hello</h1>")
    return render(
        request,
        "all_rooms.html",
        context={"message": msg, "now": now, "hungry": hungry},
    )
