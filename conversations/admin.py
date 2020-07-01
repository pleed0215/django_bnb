from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """ Conversation admin difinition """

    pass


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    """ Message admin difinition """

    pass
