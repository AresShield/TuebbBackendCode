from django.db import models
from userAuth.models import VenueProfile, CustomUser
import os
from django.dispatch import receiver
from django.db.models.signals import post_save


# represent items on the menu
class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True, null=True)
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
    file = models.ImageField(upload_to='uploads/')

@receiver(models.signals.post_delete, sender=Photo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

class AdvancedVenueProfile(models.Model):
    venue_profile = models.ForeignKey(VenueProfile, on_delete=models.CASCADE, related_name="advanced_profile")
    address = models.CharField(max_length=200, blank=True, null=True)
    opening_hours = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    contact = models.CharField(max_length=200, blank=True, null=True)
    images = models.ManyToManyField(Photo, related_name="venue", blank=True)
    entry_fee = models.FloatField(blank=True, null=True)
    team = models.ManyToManyField(CustomUser, related_name="venue", blank=True)
    def __str__(self):
        return f"Company profile of {self.venue_profile.company_name}"

@receiver(post_save, sender=VenueProfile)
def create_dependecies(sender, instance, created, **kwargs):
    if created:
        AdvancedVenueProfile.objects.create(venue_profile=instance)
