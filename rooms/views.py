import math
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.urls import reverse
from .models import Room, RoomType, Amenity, Facility, HouseRule
from .forms import SearchForm

from django_countries import countries

# third way. make list.
class HomeView(ListView):
    """ HomeView definition """

    model = Room
    paginate_by = 10
    ordering = ['created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


class RoomDetailView(DetailView):
    """ DetailView definition """

    model = Room


"""  ---------------------------------------------------- """


def if_none_default(value, default):
    return value is not None and value or default


# class 형태로 바꾸고 싶다면.. class SearchView(View): get method를 아래 함수로 오버라이딩하면 된다.
def search_view(request):

    forms = SearchForm(request.GET)
    rooms = None
    uri = request.get_raw_uri()
    if forms.is_valid():
        city = forms.cleaned_data.get("city")
        country = forms.cleaned_data.get("country")
        min_price = forms.cleaned_data.get("min_price")
        max_price = forms.cleaned_data.get("max_price")
        room_type = forms.cleaned_data.get("room_type")
        guests = forms.cleaned_data.get("guests")
        baths = forms.cleaned_data.get("baths")
        beds = forms.cleaned_data.get("beds")
        bedrooms = forms.cleaned_data.get("bedrooms")
        instant_book = forms.cleaned_data.get("instant_book")
        superhost = forms.cleaned_data.get("superhost")
        amenities = forms.cleaned_data.get("amenities")
        facilities = forms.cleaned_data.get("facilities")

        filtering = {}

        # city filtering
        if city != "Anywhere":
            filtering["city__startswith"] = city

        if country:
            filtering["country"] = country

        # filter with price
        if min_price is not None and max_price is not None:
            filtering["price__gte"] = min_price
            filtering["price__lte"] = max_price

        # room type filtering
        if room_type is not None:
            filtering["room_type"] = room_type

        # guests, beds, bedrooms, baths filtering
        if guests is not None:
            filtering["guests__gte"] = guests
        if beds is not None:
            filtering["beds__gte"] = beds
        if bedrooms is not None:
            filtering["bedrooms__gte"] = bedrooms
        if baths is not None:
            filtering["baths__gte"] = baths
        # instant book filtering
        if instant_book is not None:
            filtering["instant_book"] = instant_book
        # superhost filtering
        if superhost is not None:
            filtering["host__is_superhost"] = superhost

        print(filtering)
        mtom_filter = Room.objects.filter()

        for c in amenities:
            mtom_filter = mtom_filter.filter(amenities=c)

        for c in facilities:
            mtom_filter = mtom_filter.filter(facilities=c)

        qs = mtom_filter.filter(**filtering).order_by("created_at")
        paginator = Paginator(qs, 10, allow_empty_first_page=True)
        page = int(request.GET.get("page", 1))
        rooms = paginator.page(page)
        print(filtering)
        print(rooms)
    else:
        forms = SearchForm()

    return render(
        request,
        "rooms/search.html",
        context={"forms": forms, "rooms": rooms, "uri": uri},
    )


# django form을 이용해야 하기 때문에.. 얘는 빠이빠이..
"""def search_view(request):
    city = request.GET.get("city", "anywhere")
    city = city == "" and "anywhere" or city
    country = request.GET.get("country", "AnyCountry")

    room_type = request.GET.get("room_type", 0)
    room_type = int(room_type)

    min_price = request.GET.get("min_price")
    min_price = min_price and int(min_price) or 10

    max_price = request.GET.get("max_price")
    max_price = max_price and int(max_price) or 100

    guests = request.GET.get("guests")
    guests = guests and int(guests) or 1

    beds = request.GET.get("beds")
    beds = beds and int(beds) or 1

    baths = request.GET.get("baths")
    baths = baths and int(baths) or 1

    bedrooms = request.GET.get("bedrooms")
    bedrooms = bedrooms and int(bedrooms) or 1

    checked_amenities = request.GET.getlist("amenities")
    checked_facilities = request.GET.getlist("facilities")

    is_instant = bool(request.GET.get("instant", False))
    is_superhost = bool(request.GET.get("superhost", False))

    room_types = RoomType.objects.all()
    amenities = Amenity.objects.all()
    facilities = Facility.objects.all()
    house_rules = HouseRule.objects.all()

    filtering = {}

    # city filtering
    if city != "anywhere":
        filtering["city__startswith"] = city

    if country != "AnyCountry":
        filtering["country"] = country

    # filter with price
    filtering["price__gte"] = min_price
    filtering["price__lte"] = max_price

    # room type filtering
    if room_type != 0:
        filtering["room_type_id"] = room_type

    # guests, beds, bedrooms, baths filtering
    if guests != 0:
        filtering["guests__gte"] = guests
    if beds != 0:
        filtering["beds__gte"] = beds
    if bedrooms != 0:
        filtering["bedrooms__gte"] = bedrooms
    if baths != 0:
        filtering["baths__gte"] = baths
    # instant book filtering
    filtering["instant_book"] = is_instant
    # superhost filtering
    filtering["host__is_superhost"] = is_superhost

    mtom_filter = Room.objects.filter()
    if len(checked_amenities) > 0:
        for c in checked_amenities:
            mtom_filter = mtom_filter.filter(amenities__pk=int(c))

    print(room_type)
    print(filtering)

    rooms = mtom_filter.filter(**filtering)
    print(rooms)

   
    # 밑에 코드(for문 두개)는 주석처리 해야 한다. 이 삽질은 잘못된 삽질입니다. getlist를 이용하십시오... 퍼킹..
    for a in amenities:
        is_checked = bool(request.GET.get(f"a_{a.pk}"))
        if is_checked is True:
            checked_amenities.append(a.pk)

    for f in facilities:
        is_checked = bool(request.GET.get(f"f_{f.pk}"))
        if is_checked is True:
            checked_facilities.append(f.pk)
    
    form = {
        "room_types": room_types,
        "countries": countries,
        "city": city,
        "amenities": amenities,
        "facilities": facilities,
        "house_rules": house_rules,
    }

    selected = {
        "s_room_type": room_type,
        "s_country": country,
        "min_price": min_price,
        "max_price": max_price,
        "guests": guests,
        "beds": beds,
        "baths": baths,
        "bedrooms": bedrooms,
        "checked_amenities": checked_amenities,
        "checked_facilities": checked_facilities,
        "is_superhost": is_superhost,
        "is_instant": is_instant,
    }

    if city != "":
        city = str.capitalize(city)
    else:
        city = "Anywhere"
    return render(
        request, "rooms/search.html", context={**form, **selected, "rooms": rooms},
    )"""


def detail_view(request, pk):
    try:
        room = Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except Room.DoesNotExist:
        # return redirect(reverse("core:home"))
        raise Http404()


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
