from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import menu_item_view, menu_view, adv_venue_profile_view, change_team_members_view, is_team_member_view
from rest_framework.test import force_authenticate
from .models import Menu, MenuItem, AdvancedVenueProfile
from userAuth.models import VenueProfile
import tempfile
from PIL import Image as ImageFile

"""
Regarding the tests:
I will add way more tests later. They don't cover everything yet.
They also don't follow the DRY principle. I will change that too. 
"""


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


class AdvancedVenueProfileTests(TestCase):
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
        self.adv_profile = self.venue.advanced_profile.all()[0]
        self.adv_profile.address = "New York 2"
        self.adv_profile.opening_hours = "Fri - Mon; 8pm - 6 am"
        self.adv_profile.description = "Best night club in city"
        self.adv_profile.contact = "examplevenue@gmail.com"
        self.adv_profile.entry_fee = 15.2
        self.adv_profile.save()

    def test_retrieving_info_from_others(self):
        request = self.request_factory.get(f'/adv_profile/{self.adv_profile.id}', format='json')
        request.user = self.user1
        response = adv_venue_profile_view(request, pk=self.adv_profile.id)
        self.assertEqual(response.data.get("address"), "New York 2")
        self.assertEqual(response.data.get("entry_fee"), 15.2)

    def test_retrieving_info_from_own_venue(self):
        request = self.request_factory.get(f'/adv_profile/', format='json')
        request.user = self.user
        response = adv_venue_profile_view(request)
        self.assertEqual(response.data.get("address"), "New York 2")
        self.assertEqual(response.data.get("entry_fee"), 15.2)

    def test_updating_string_info(self):
        request = self.request_factory.put(f'/adv_profile/', {"address": "New York 1", "opening_hours": "updated!",
                                                              "description": "updated_desc", "contact": "updated contact",
                                                              "entry_fee": 17.23}, format='json')
        request.user = self.user
        response = adv_venue_profile_view(request)
        #print("message: "+str(response.data))
        self.adv_profile = AdvancedVenueProfile.objects.get(venue_profile=self.venue)
        self.assertEqual(self.adv_profile.address, "New York 1")
        self.assertEqual(self.adv_profile.entry_fee, 17.23)

    def test_updating_string_info_without_permission(self):
        request = self.request_factory.put(f'/adv_profile/{self.adv_profile.id}', {"address": "New York 1", "opening_hours": "updated!",
                                                              "description": "updated_desc", "contact": "updated contact",
                                                              "entry_fee": 17.23}, format='json')
        request.user = self.user2
        response = adv_venue_profile_view(request, pk=self.adv_profile.id)
        #print("message: "+str(response.data))
        self.adv_profile = AdvancedVenueProfile.objects.get(venue_profile=self.venue)
        self.assertEqual(self.adv_profile.address, "New York 2")

    def test_upload_image(self):
        image = ImageFile.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image_file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(image_file, 'png')
        #image_file.seek(0)

        with open(image_file.name, 'rb') as image:
            # Upload the image.
            data = {
                'upload_image': image, "address": "New York 1", "opening_hours": "updated!",
                "description": "updated_desc", "contact": "updated contact",
                "entry_fee": 17.23
            }

            request = self.request_factory.put('/adv_profile/', data, format='multipart')
            request.user = self.user
            response = adv_venue_profile_view(request)
            self.adv_profile = AdvancedVenueProfile.objects.get(venue_profile=self.venue)
            self.assertTrue(len(self.adv_profile.images.all())==1)
        self.adv_profile.images.all().delete()

    def test_delete_images(self):
        image = ImageFile.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image_file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(image_file, 'png')
        # image_file.seek(0)

        with open(image_file.name, 'rb') as image:
            # Upload the image.
            data = {
                'upload_image': image, "address": "New York 1", "opening_hours": "updated!",
                "description": "updated_desc", "contact": "updated contact",
                "entry_fee": 17.23
            }

            request = self.request_factory.put('/adv_profile/', data, format='multipart')
            request.user = self.user
            response = adv_venue_profile_view(request)
            self.adv_profile = AdvancedVenueProfile.objects.get(venue_profile=self.venue)
            self.assertTrue(len(self.adv_profile.images.all()) == 1)

            data = {
                'delete_photos': [self.adv_profile.images.all()[0].id], "address": "New York 1", "opening_hours": "updated!",
                "description": "updated_desc", "contact": "updated contact",
                "entry_fee": 17.23
            }

            request = self.request_factory.put('/adv_profile/', data, format='multipart')
            request.user = self.user
            response = adv_venue_profile_view(request)
            self.adv_profile = AdvancedVenueProfile.objects.get(venue_profile=self.venue)
            self.assertTrue(len(self.adv_profile.images.all()) == 0)


class ChangeTeamMembersTests(TestCase):

    def setUp(self):
        self.request_factory = APIRequestFactory()
        # venue owner
        self.user = get_user_model().objects.create_user(
            email='javed@javed.com', password='my_secret')
        # team member
        self.user1 = get_user_model().objects.create_user(
            email='bert@bert.com', password='my_secret')
        # 3rd party user
        self.user2 = get_user_model().objects.create_user(
            email='anna@anna.com', password='my_secret')
        self.venue = VenueProfile.objects.create(company_name="ExampleVenue", unique_code="12345",
                                                 govern_user=self.user)
        self.adv_profile = self.venue.advanced_profile.all()[0]
        self.adv_profile.address = "New York 2"
        self.adv_profile.opening_hours = "Fri - Mon; 8pm - 6 am"
        self.adv_profile.description = "Best night club in city"
        self.adv_profile.contact = "examplevenue@gmail.com"
        self.adv_profile.entry_fee = 15.2
        self.adv_profile.save()

    def test_adding_user(self):

        data = {
            "add_team_member": "bert@bert.com"
        }

        request = self.request_factory.patch(f'/change_team_members/', data, format='json')
        request.user = self.user
        response = change_team_members_view(request)
        self.assertTrue(len(response.data.get("team"))==1)

    def test_removing_user(self):
        data = {
            "add_team_member": "bert@bert.com"
        }

        request = self.request_factory.patch(f'/change_team_members/', data, format='json')
        request.user = self.user
        response = change_team_members_view(request)

        data = {
            "remove_team_member": "bert@bert.com"
        }
        request = self.request_factory.patch(f'/change_team_members/', data, format='json')
        request.user = self.user
        response = change_team_members_view(request)
        self.assertTrue(len(response.data.get("team")) == 0)


    def test_is_team_member_yes(self):
        self.adv_profile.team.add(self.user2)
        self.adv_profile.save()
        request = self.request_factory.get(f'/is-team-member/', format='json')
        request.user = self.user2
        response = is_team_member_view(request)
        self.assertTrue(response.data.get("result")=="YES")

    def test_is_team_member_no(self):
        request = self.request_factory.get(f'/is-team-member/', format='json')
        request.user = self.user1
        response = is_team_member_view(request)
        self.assertTrue(response.data.get("result") == "NO")
