from django.contrib import admin
from .models import VenueWallet, Wallet, ConsumerWallet

# Register your models here.
admin.site.register(VenueWallet)
admin.site.register(Wallet)
admin.site.register(ConsumerWallet)
