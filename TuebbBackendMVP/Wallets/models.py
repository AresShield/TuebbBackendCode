from django.db import models
from django.contrib.auth import get_user_model
from userAuth.models import VenueProfile
from ConsumerPart.models import ConsumerUser
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Wallet(models.Model):
    balance = models.FloatField(default=0)

class VenueWallet(Wallet):
    owner = models.ForeignKey(VenueProfile, on_delete=models.CASCADE, related_name="wallet")

class ConsumerWallet(Wallet):
    owner = models.ForeignKey(ConsumerUser, on_delete=models.CASCADE, related_name="wallet")


@receiver(post_save, sender=ConsumerUser)
def create_consumer_wallet(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user profile object is created."""
    if created:
        ConsumerWallet.objects.create(owner=instance, balance=0.0)

@receiver(post_save, sender=VenueProfile)
def create_venue_wallet(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user profile object is created."""
    if created:
        VenueWallet.objects.create(owner=instance, balance=0.0)
