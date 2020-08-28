import uuid
import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.managers import CustomUserManager


# Create your models here.
class User(AbstractUser):
    """ Custom user model """

    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"
    GENDER_OTHER = "Other"

    GENDER_CHOICE = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANG_KOR = "KR"
    LANG_ENG = "EN"
    LANG_CHOICE = ((LANG_KOR, _("Korean")), (LANG_ENG, _("English")))

    CURRENCY_USD = "USD"
    CURRENCY_KRW = "KRW"
    CURRENCY_CHOICE = ((CURRENCY_USD, _("US dollor")),
                       (CURRENCY_KRW, _("Korea Won")))

    LOGIN_METHOD_EMAIL = "EM"
    LOGIN_METHOD_GITHUB = "GH"
    LOGIN_METHOD_KAKAO = "KK"
    LOGIN_METHOD_CHOICE = (
        (LOGIN_METHOD_EMAIL, "Email"),
        (LOGIN_METHOD_GITHUB, "Github"),
        (LOGIN_METHOD_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(_("avatar"), blank=True, upload_to="avatars")
    gender = models.CharField(
        _("gender"), choices=GENDER_CHOICE, max_length=10, blank=True)
    bio = models.TextField(_("bio"), blank=True, default="")
    birthday = models.DateField(_("birthday"), null=True, blank=True)
    language = models.CharField(_("language"),
                                choices=LANG_CHOICE, max_length=2, blank=True, default=LANG_KOR
                                )
    currency = models.CharField(_("currency"),
                                choices=CURRENCY_CHOICE, max_length=3, blank=True, default=CURRENCY_KRW
                                )
    is_superhost = models.BooleanField(_("is superhost"), default=False)
    email_verified = models.BooleanField(_("email verified"), default=False)
    email_secret = models.CharField(max_length=128, default="")
    login_method = models.CharField(
        max_length=2, choices=LOGIN_METHOD_CHOICE, default=LOGIN_METHOD_EMAIL
    )

    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse("users:user", kwargs={"pk": self.pk})

    def verify_email(self):
        if self.email_verified is True:
            pass
        else:
            self.email_secret = uuid.uuid4().hex[:20]
            self.save()
            # using template file instead.
            link = f"{os.environ.get('SITE_URL')}/users/verify/{self.email_secret}"
            html_msg = render_to_string(
                "mail_body.html", context={"link": link})
            # html_msg = f'<p>This is just verficiatino mail and do not reply.</p><p>To verify click <a href="http://127.0.0.1:8000/users/{self.email_secret}">here</a></p>'
            send_mail(
                _("Hello, from DjangoBnB, account verification mail!"),
                strip_tags(html_msg),
                "pleed0215@gmail.com",
                [self.email, ],
                fail_silently=False,
                html_message=html_msg,
            )
