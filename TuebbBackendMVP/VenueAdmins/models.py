from django.db import models
from userAuth.models import VenueProfile


# represent items on the menu
class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    price = models.FloatField()

    def __str__(self):
        return self.name


# represent the whole menu of a venue
# Create your models here.
class Menu(models.Model):
    owner = models.ForeignKey(VenueProfile, on_delete=models.CASCADE, related_name="menu")
    items = models.ManyToManyField(MenuItem, related_name="menues", blank=True)

    def __str__(self):
        return self.owner.company_name



# Venue profile settings
class Photo(models.Model):
    file = models.FileField(upload_to='uploads/')

    def delete(self):
        self.file.delete()
        super().delete()

class AdvancedVenueProfile(models.Model):
    venue_profile = models.ForeignKey(VenueProfile, on_delete=models.CASCADE, related_name="advanced_profile")
    address = models.CharField(max_length=200)
    opening_hours = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    contact = models.CharField(max_length=200)
    images = models.ManyToManyField(Photo, related_name="venue", blank=True)

    def __str__(self):
        return f"Company profile of {self.venue_profile.company_name}"
