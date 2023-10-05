from django.urls import path
from .views import consumer_account_creation_view, ConsumerProfileView


app_name = "CheckInProcess"

urlpatterns = [
    path('consumer-account-creation/', consumer_account_creation_view, name='consumer_creation'),
    path('consumer-account-updates/', ConsumerProfileView.as_view(), name='consumer_updates')
]
