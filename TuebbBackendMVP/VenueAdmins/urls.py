from django.urls import path
from .views import menu_view, menu_item_view, adv_venue_profile_view, change_team_members_view, is_team_member_view


app_name = "VenueAdmins"

urlpatterns = [
    path('menu_item/<int:pk>/', menu_item_view, name='menu_item'),
    path('menu/<int:pk>', menu_view, name='menu'),
    path('menu_item/', menu_item_view, name='menu_item_without'),
    path('menu/', menu_view, name='menu_without'),
    path('adv_profile/<int:pk>', adv_venue_profile_view, name='adv_profile'),
    path('adv_profile/', adv_venue_profile_view, name='adv_profile_without'),
    path('change_team_members/', change_team_members_view, name="change_team"),
    path('is-team-member/', is_team_member_view, name="is_team_member")
]
