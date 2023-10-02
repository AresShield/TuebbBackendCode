from django.urls import path
from .views import RegisterView, valid_user, link_account_to_venue
app_name = "userAuth"


urlpatterns = [
    path('login/', valid_user, name='auth_login'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('link-venue-profile/', link_account_to_venue, name="link_venue_profile")
]
