from django.contrib import admin
from .models import MenuItem, Menu, AdvancedVenueProfile, Photo


# Register your models here.
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(AdvancedVenueProfile)
admin.site.register(Photo)
