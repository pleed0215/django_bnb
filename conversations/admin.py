from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """ Conversation admin difinition """

    list_display = ("__str__", "created_at", "get_num_messages")


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    """ Message admin difinition """

    list_display = (
        "__str__",
        "created_at",
    )
