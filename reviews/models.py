from django.db import models
from core.models import AbstractTimeStamped

# Create your models here.
class Review(AbstractTimeStamped):
    """ Review model definition """

    review = models.TextField()

    # evaluation points
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()

    # Forein Key
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s review of {self.room.name}"
