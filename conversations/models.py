from django.db import models
from core.models import AbstractTimeStamped

# Create your models here.
class Conversation(AbstractTimeStamped):
    """ Conversation Model definition """

    participants = models.ManyToManyField(
        "users.User", related_name="my_conversations", blank=False
    )

    def __str__(self):
        joined_user = []
        for p in self.participants.all():
            joined_user.append(p.username)
        text = "Conersations of [" + ", ".join(joined_user) + "]"

        return text

    def get_num_messages(self):
        return self.my_messages.count()

    get_num_messages.short_description = "n. msgs"


class Message(AbstractTimeStamped):
    """ Definition of Message Model """

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="my_messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        Conversation, related_name="my_messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.created_at}: {self.user}'s message: {self.message}'"

