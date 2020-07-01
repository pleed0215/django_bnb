from django.db import models
from core.models import AbstractTimeStamped

# Create your models here.
class List(AbstractTimeStamped):

    """ definition of List Model """

    name = models.CharField(max_length=80)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    rooms = models.ManyToManyField("rooms.Room", blank=True)

    def __str__(self):
        return f"{self.name} - list of {self.user}"
