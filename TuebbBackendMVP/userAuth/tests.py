from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import valid_user, link_account_to_venue
from rest_framework.test import force_authenticate
from .models import VenueProfile


# Test User Creation of our custom user model
class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)


# test login credentials checks
class UserBehaviourTests(TestCase):

    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email='javed@javed.com', password='my_secret')

    # no auth credentials provided, therefore should fail!
    def test_login_verification_failed(self):
        request = self.request_factory.post('/login/')
        response = valid_user(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_verification_success(self):
        request = self.request_factory.post('/login/')
        request.user = self.user
        response = valid_user(request)
        self.assertEqual(response.data, {"Status": "Valid User!"})


# test venues admin account linking
class AdminAccountTests(TestCase):
    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email='javed@javed.com', password='my_secret')
        self.user1 = get_user_model().objects.create_user(
            email='bert@bert.com', password='my_secret')
        self.venue = VenueProfile.objects.create(company_name="ExampleVenue", unique_code="12345")

    def test_linking(self):
        request = self.request_factory.post('/link_venue_profile/', {'unique_code': '12345'}, format='json')
        request.user = self.user
        response = link_account_to_venue(request)
        self.assertTrue(response.status_code==status.HTTP_202_ACCEPTED)
        self.venue = VenueProfile.objects.get(unique_code="12345")
        self.assertEqual(self.user, self.venue.govern_user)

    def test_use_unique_code_twice(self):
        request = self.request_factory.post('/link_venue_profile/', {'unique_code': '12345'}, format='json')
        request.user = self.user
        response = link_account_to_venue(request)
        #self.assertTrue(response.status_code == status.HTTP_202_ACCEPTED)
        request = self.request_factory.post('/link_venue_profile/', {'unique_code': '12345'}, format='json')
        request.user = self.user1
        response = link_account_to_venue(request)
        self.venue = VenueProfile.objects.get(unique_code="12345")
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
