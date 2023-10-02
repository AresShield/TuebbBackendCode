from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import menu_item_view, menu_view
from rest_framework.test import force_authenticate
from .models import Menu, MenuItem
from userAuth.models import VenueProfile

# Create your tests here.
class MenuAndMenuItemTesting(TestCase):
    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email='javed@javed.com', password='my_secret')
        self.user1 = get_user_model().objects.create_user(
            email='bert@bert.com', password='my_secret')
        self.user2 = get_user_model().objects.create_user(
            email='anna@anna.com', password='my_secret')
        self.venue = VenueProfile.objects.create(company_name="ExampleVenue", unique_code="12345", govern_user=self.user)
        self.venue1 = VenueProfile.objects.create(company_name="ExampleVenue", unique_code="123456",
                                                 govern_user=self.user2)
        self.menu = Menu.objects.create(owner=self.venue)
        self.menu1 = Menu.objects.create(owner=self.venue1)


    def test_adding_item(self):
        request = self.request_factory.post('/menu_item/', {"name": "TestDrink", "description":"15% alk, don't overdo it bro", "price": "15.432"}, format='json')
        request.user = self.user
        view = menu_item_view
        response = view(request)
        self.assertTrue(response.status_code==status.HTTP_201_CREATED)
        self.assertTrue(self.menu.items.all()[0].name=="TestDrink")
        request = self.request_factory.post('/menu_item/',
                                            {"name": "TestDrink1", "description": "30% alk, don't overdo it bro",
                                             "price": 32.432}, format='json')
        request.user = self.user
        response = view(request)
        self.assertTrue(response.status_code == status.HTTP_201_CREATED)
        self.assertTrue(self.menu.items.all()[1].description == "30% alk, don't overdo it bro")

    def test_adding_without_auth(self):
        request = self.request_factory.post('/menu_item/',
                                                {"name": "TestDrink", "description": "15% alk, don't overdo it bro",
                                                 "price": "15.432"}, format='json')

        request.user = self.user1
        view = menu_item_view
        response = view(request)
        self.assertTrue(response.status_code == status.HTTP_403_FORBIDDEN)


    def test_updating_item(self):
        request = self.request_factory.post('/menu_item/',
                                            {"name": "TestDrink", "description": "15% alk, don't overdo it bro",
                                             "price": "15.432"}, format='json')
        request.user = self.user
        view = menu_item_view
        response = view(request)
        self.assertTrue(self.menu.items.all()[0].name == "TestDrink")
        request = self.request_factory.put(f'/menu_item/{response.data.get("id")}',
                                            {"name": "TestDrink1", "description": "15% alk, don't overdo it bro",
                                             "price": "14.432"}, format='json')
        request.user = self.user
        view = menu_item_view
        response = view(request, pk=response.data.get("id"))
        self.assertEqual(len(self.menu.items.all()),1)
        self.assertEqual(self.menu.items.all()[0].name,"TestDrink1")
        self.assertEqual(self.menu.items.all()[0].price, 14.432)


    def test_retrieving_menu(self):
        request = self.request_factory.post('/menu_item/',
                                            {"name": "TestDrink", "description": "15% alk, don't overdo it bro",
                                             "price": "15.432"}, format='json')
        request.user = self.user
        view = menu_item_view
        response = view(request)
        request = self.request_factory.get(f'/menu/{response.data.get("id")}', format='json')
        request.user = self.user1
        view = menu_view
        response = view(request, pk=response.data.get("id"))
        self.assertEqual(response.data.get("items")[0]["name"],"TestDrink")

        request = self.request_factory.post('/menu_item/',
                                            {"name": "TestDrink23", "description": "15% alk, don't overdo it bro",
                                             "price": "15.432"}, format='json')
        request.user = self.user2
        view = menu_item_view
        response = view(request)
        request = self.request_factory.get(f'/menu/{response.data.get("id")}', format='json')
        request.user = self.user1
        view = menu_view
        response = view(request, pk=response.data.get("id"))
        self.assertEqual(response.data.get("items")[0]["name"], "TestDrink23")

    def test_retrieving_menu_without_pk(self):
        request = self.request_factory.post('/menu_item/',
                                            {"name": "TestDrink", "description": "15% alk, don't overdo it bro",
                                             "price": "15.432"}, format='json')
        request.user = self.user
        view = menu_item_view
        response = view(request)
        request = self.request_factory.get(f'/menu/', format='json')
        request.user = self.user
        view = menu_view
        response = view(request)
        self.assertEqual(response.data.get("items")[0]["name"],"TestDrink")

        request = self.request_factory.post('/menu_item/',
                                            {"name": "TestDrink23", "description": "15% alk, don't overdo it bro",
                                             "price": "15.432"}, format='json')
        request.user = self.user2
        view = menu_item_view
        response = view(request)
        request = self.request_factory.get(f'/menu/', format='json')
        request.user = self.user2
        view = menu_view
        response = view(request)
        self.assertEqual(response.data.get("items")[0]["name"], "TestDrink23")

    def test_retrieving_menu_without_pk_without_permission(self):
        request = self.request_factory.post('/menu_item/',
                                            {"name": "TestDrink", "description": "15% alk, don't overdo it bro",
                                             "price": "15.432"}, format='json')
        request.user = self.user
        view = menu_item_view
        response = view(request)
        request = self.request_factory.get(f'/menu/', format='json')
        request.user = self.user1
        view = menu_view
        response = view(request)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

        request = self.request_factory.post('/menu_item/',
                                            {"name": "TestDrink23", "description": "15% alk, don't overdo it bro",
                                             "price": "15.432"}, format='json')
        request.user = self.user2
        view = menu_item_view
        response = view(request)
        request = self.request_factory.get(f'/menu/', format='json')
        request.user = self.user
        view = menu_view
        response = view(request)
        self.assertEqual(response.data.get("items")[0]["name"], "TestDrink")


    def test_deleting_item_wrong_auth(self):
        request = self.request_factory.post('/menu_item/',
                                            {"name": "TestDrink23", "description": "15% alk, don't overdo it bro",
                                             "price": "15.432"}, format='json')
        request.user = self.user2
        view = menu_item_view
        response = view(request)
        self.assertTrue(len(self.menu1.items.all())==1)
        request = self.request_factory.patch(f'/menu/', {"delete_menu_items": [response.data.get("id")]},format='json')
        request.user = self.user
        view = menu_view
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(self.menu1.items.all()),1)

    def test_deleting_item(self):
        request = self.request_factory.post('/menu_item/',
                                            {"name": "TestDrink23", "description": "15% alk, don't overdo it bro",
                                             "price": "15.432"}, format='json')
        request.user = self.user2
        view = menu_item_view
        response = view(request)
        self.assertTrue(len(self.menu1.items.all())==1)
        request = self.request_factory.patch(f'/menu/', {"delete_menu_items": [response.data.get("id"),]},format='json')
        request.user = self.user2
        view = menu_view
        response = view(request)
        self.assertTrue(len(self.menu1.items.all())==0)
