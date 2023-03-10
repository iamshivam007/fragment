from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for telegram.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    name = CharField(_("Name of User"), blank=True, max_length=255)
    country_code = CharField(_("User Country Code"), blank=True, max_length=4)
    mobile_number = CharField(_("Mobile Number"), max_length=10, null=True, unique=True)
    login_otp = CharField(_("Login OTP"), blank=True, max_length=10)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    last_sync = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.name} -> ${self.mobile_number}"
