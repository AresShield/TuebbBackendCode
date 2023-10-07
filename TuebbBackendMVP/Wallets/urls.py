from django.urls import path
from .views import get_balance_view, load_up_money_view, pay_out_money_view


app_name = "Wallets"

urlpatterns = [
    path('get-wallet-balance/', get_balance_view, name='get_balance'),
    path("load-up/", load_up_money_view, name="load_up"),
    path("pay_out/", pay_out_money_view, name="pay_out"),
]
