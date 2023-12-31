from django.db import models
from VenueAdmins.models import AdvancedVenueProfile
from django.contrib.auth import get_user_model

# Create your models here.

# NOTE: We really need to implement chargebacks and all of that stuff
class Ticket(models.Model):
    creator = models.ForeignKey(AdvancedVenueProfile, on_delete=models.CASCADE, related_name="tickets")
    price = models.FloatField()
    paid = models.BooleanField(default=False)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="tickets", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        if self.owner:
            return f"Paid {self.owner.email} | {self.pk} | {self.creator.venue_profile.company_name}"
        else:
            return f"Unpaid | {self.pk} | {self.creator.venue_profile.company_name}"
