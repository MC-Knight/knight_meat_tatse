from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager
from django.conf import settings


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, "Client"),
        (2, "Cashier"),
        (3, "Admin"),
    )

    username = None
    email = models.EmailField(_("email address"), unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    email_token = models.CharField(max_length=255, null=True, blank=True)
    is_verfied = models.BooleanField(default=False)
    password_reset_token = models.CharField(max_length=32, null=True, blank=True)
    password_reset_token_expiry = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=155, null=True, blank=True)

    # location
    address_1 = models.CharField(max_length=250, null=True, blank=True)
    address_2 = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)

    # profile picture
    profile_picture = models.ImageField(upload_to="avatars/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name != "" and self.last_name != "":
            return self.first_name + " " + self.last_name
        else:
            return self.email

    def get_user_type_display(self):
        return dict(self.USER_TYPE_CHOICES).get(self.user_type)

