from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# Create your models here.
class User(AbstractUser):
    """ Custom user model """

    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"
    GENDER_OTHER = "Other"

    GENDER_CHOICE = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANG_KOR = "KR"
    LANG_ENG = "EN"
    LANG_CHOICE = ((LANG_KOR, "Korean"), (LANG_ENG, "English"))

    CURRENCY_USD = "USD"
    CURRENCY_KRW = "KRW"
    CURRENCY_CHOICE = ((CURRENCY_USD, "US dollor"), (CURRENCY_KRW, "Korea Won"))

    avatar = models.ImageField(blank=True, upload_to="avatars")
    gender = models.CharField(choices=GENDER_CHOICE, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    language = models.CharField(choices=LANG_CHOICE, max_length=2, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICE, max_length=3, blank=True)
    is_superhost = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("users:user", kwargs={"pk": self.pk})

