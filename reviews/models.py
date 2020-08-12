from django.db import models
from core.models import AbstractTimeStamped
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Review(AbstractTimeStamped):
    """ Review model definition """

    review = models.TextField()

    # evaluation points
    accuracy = models.IntegerField(
        validators=[
            MinValueValidator(0, "Must greater than 0"),
            MaxValueValidator(5, "Must be under 5"),
        ]
    )
    communication = models.IntegerField(
        validators=[
            MinValueValidator(0, "Must greater than 0"),
            MaxValueValidator(5, "Must be under 5"),
        ]
    )
    cleanliness = models.IntegerField(
        validators=[
            MinValueValidator(0, "Must greater than 0"),
            MaxValueValidator(5, "Must be under 5"),
        ]
    )
    location = models.IntegerField(
        validators=[
            MinValueValidator(0, "Must greater than 0"),
            MaxValueValidator(5, "Must be under 5"),
        ]
    )
    check_in = models.IntegerField(
        validators=[
            MinValueValidator(0, "Must greater than 0"),
            MaxValueValidator(5, "Must be under 5"),
        ]
    )
    value = models.IntegerField(
        validators=[
            MinValueValidator(0, "Must greater than 0"),
            MaxValueValidator(5, "Must be under 5"),
        ]
    )

    # Foreign Key
    user = models.ForeignKey(
        "users.User", related_name="my_reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="my_reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username}'s review of {self.room.name}"

    def rating_average(self):
        avg = (
            float(
                self.accuracy
                + self.communication
                + self.cleanliness
                + self.location
                + self.check_in
                + self.value
            )
            / 6
        )
        return round(avg, 2)

    rating_average.short_description = "ratings"

    class Meta:
        ordering = ("-created_at",)
