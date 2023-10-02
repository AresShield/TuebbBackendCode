from django.urls import path
from .views import menu_view, menu_item_view#, menu_view_without_arguments


app_name = "VenueAdmins"

urlpatterns = [
    path('menu_item/<int:pk>/', menu_item_view, name='menu_item'),
    path('menu/<int:pk>', menu_view, name='menu'),
    path('menu_item/', menu_item_view, name='menu_item_without'),
    path('menu/', menu_view, name='menu_without'),
]
