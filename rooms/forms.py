from django import forms
from .models import RoomType, Amenity, Facility

from django_countries.fields import CountryField


class SearchForm(forms.Form):
    city = forms.CharField(required=False, initial="Anywhere",)
    country = CountryField(blank=True).formfield()
    min_price = forms.IntegerField(required=False, initial=10)
    max_price = forms.IntegerField(required=False, initial=1000)
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=RoomType.objects.all()
    )

    guests = forms.IntegerField(required=False, initial=1)
    baths = forms.IntegerField(required=False, initial=1)
    beds = forms.IntegerField(required=False, initial=1)
    bedrooms = forms.IntegerField(required=False, initial=1)

    instant_book = forms.BooleanField(required=False, initial=False)
    superhost = forms.BooleanField(required=False, initial=False)

    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        queryset=Facility.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
