from django.urls import path
from .views import ticket_creation_view


app_name = "CheckInProcess"

urlpatterns = [
    path('ticket-creation/', ticket_creation_view, name='ticket_creation'),
]
