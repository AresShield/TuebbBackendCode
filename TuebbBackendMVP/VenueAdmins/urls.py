from django.urls import path
from .views import menu_view, menu_item_view, adv_venue_profile_view


app_name = "VenueAdmins"

urlpatterns = [
    path('menu_item/<int:pk>/', menu_item_view, name='menu_item'),
    path('menu/<int:pk>', menu_view, name='menu'),
    path('menu_item/', menu_item_view, name='menu_item_without'),
    path('menu/', menu_view, name='menu_without'),
    path('adv_profile/<int:pk>', adv_venue_profile_view, name='adv_profile'),
    path('adv_profile/', adv_venue_profile_view, name='adv_profile_without'),
]
