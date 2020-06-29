from django.contrib import admin
from . import models


# Register your models here.

# 아래처럼 여러개를 만들 필요 없다.
@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class AbstractItem(admin.ModelAdmin):
    pass


"""
@admin.register(models.RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Facility)
class FacilityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.HouseRule)
class HouseRuleAdmin(admin.ModelAdmin):
    pass
"""


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Room basic information", {"fields": ("name", "description",)}),
        ("Additional information", {"fields": ("country", "city", "price", "address")}),
        (
            "Rooms facialities information",
            {"fields": ("guests", "beds", "bedrooms", "baths", "room_type",)},
        ),
        (
            "Booking information",
            {"fields": ("check_in", "check_out", "instant_book", "host")},
        ),
    )
