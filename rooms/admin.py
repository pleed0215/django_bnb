from django.contrib import admin
from . import models


# Register your models here.

# 아래처럼 여러개를 만들 필요 없다.
@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class AbstractItem(admin.ModelAdmin):

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.my_rooms.count()


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
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
    )
    list_filter = (
        "room_type",
        "amenities",
        "facilities",
        "host__gender",
        "host__is_superhost",
        "house_rules",
        "instant_book",
        "city",
        "beds",
        "country",
    )

    fieldsets = (
        ("Room basic information", {"fields": ("name", "description",)}),
        ("Additional information", {"fields": ("country", "city", "price", "address")}),
        (
            "Rooms facialities information",
            {
                "fields": (
                    "guests",
                    "beds",
                    "bedrooms",
                    "baths",
                    "room_type",
                    "amenities",
                    "facilities",
                    "house_rules",
                )
            },
        ),
        ("Booking information", {"fields": ("check_in", "check_out", "instant_book")},),
        ("Last info.", {"classes": ("collapse",), "fields": ("host",)},),
    )
    search_fields = ("=city", "^host__username")
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )
    ordering = (
        "name",
        "price",
        "bedrooms",
    )

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "n. amenities"

    def count_photos(self, obj):
        # print(models.Photo.objects.filter(room__id=obj.id))
        return obj.my_photos.count()

    count_photos.short_description = "n. photos"

    # filter_vertical = ("amenities",)

