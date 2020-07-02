from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):
    """" ListAdmin definition In admin page """

    list_display = ("name", "user", "get_num_rooms")
    filter_horizontal = ("rooms",)
    search_fields = ("^name",)
