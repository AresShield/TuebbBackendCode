from django.urls import path
from .views import ticket_creation_view, TicketInfoView, buy_ticket_view, get_check_in_data_view


app_name = "CheckInProcess"

urlpatterns = [
    path('ticket-creation/', ticket_creation_view, name='ticket_creation'),
    path('get-ticket-info/<int:pk>', TicketInfoView.as_view(), name="ticket_info"),
    path('buy-ticket/<int:pk>', buy_ticket_view, name="ticket_buy"),
    path("get_ticket_data", get_check_in_data_view, name="get_ticket_data")
]
