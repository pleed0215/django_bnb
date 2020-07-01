from django.db import models
from core.models import AbstractTimeStamped
from django_countries.fields import CountryField


# Create your models here.
class AbstractItem(AbstractTimeStamped):
    """ Abstract model of Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract: True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """ Room type objects """

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]


class Amenity(AbstractItem):
    """ Amenity objects """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """ Facility objects """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """ House rule objects """

    pass


class Photo(AbstractTimeStamped):
    """ Photo model definition """

    caption = models.CharField(max_length=80)
    image = models.ImageField()
    room = models.ForeignKey(
        "Room", related_name="my_photos", on_delete=models.CASCADE, blank=True
    )

    def __str__(self):
        return self.caption


class Room(AbstractTimeStamped):
    """ Rooms model definitions """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)

    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)

    host = models.ForeignKey(
        "users.User", related_name="my_rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        RoomType,
        related_name="my_rooms",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    amenities = models.ManyToManyField(Amenity, related_name="my_rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="my_rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="my_rooms", blank=True)

    def __str__(self):
        return self.name
