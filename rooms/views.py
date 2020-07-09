import math
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage
from .models import Room


# Create your views here.
def all_rooms(request):
    # version of Paginator with django library.
    # look... how many lines are cut...........
    page = int(request.GET.get("page", 1))
    page_size = 9
    all_rooms = Room.objects.all()
    paginator = Paginator(all_rooms, page_size)

    # page = paginator.get_page(page)
    try:
        page = paginator.page(page)
        return render(request, "rooms/home.html", context={"page": page},)
    except EmptyPage:
        return redirect("/")

    """ # first way) only using python.
    len_rooms = Room.objects.count()
    page_size = 10
    page_remains = len_rooms % page_size
    page_remains = page_remains == 0 and page_size or page_remains
    last_page = math.ceil(len_rooms / page_size)
    start = 0
    end = 0

    if page >= last_page:
        start = (last_page - 1) * page_size
        end = start + page_remains
        page = last_page
    elif page < last_page:
        start = (page - 1) * page_size
        end = start + page_size
    else:
        start = 0
        end = start + page_size
        page = 1

    all_rooms = Room.objects.all()[start:end]
    

    # return HttpResponse(content="<h1>Hello</h1>")
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "last_page": last_page,
            "current_page": page,
            "pages": range(1, last_page + 1),
        },
    )
    """
