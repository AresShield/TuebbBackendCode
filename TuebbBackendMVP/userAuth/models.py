from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# Django user model
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



# Venue profile that we link to a user profile
class VenueProfile(models.Model):
    company_name = models.CharField(max_length=100)
    govern_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="venue_profile")
    unique_code = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.company_name


