from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import get_balance_view, load_up_money_view
from rest_framework.test import force_authenticate
from ConsumerPart.models import ConsumerUser
from userAuth.models import VenueProfile

class WalletTesting(TestCase):
    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email='javed@javed.com', password='my_secret')
        self.user1 = get_user_model().objects.create_user(
            email='bert@bert.com', password='my_secret')
        self.consumer = ConsumerUser.objects.create(user=self.user1, age=50, gender="Male")
        self.venue = VenueProfile.objects.create(company_name="ExampleVenue", govern_user=self.user, unique_code="12345")

    def test_automatic_wallet_creation_consumer(self):
        self.assertTrue(len(self.consumer.wallet.all())==1)

    def test_automatic_wallet_creation_venue(self):
        self.assertTrue(len(self.venue.wallet.all())==1)

    def test_get_balance_view_with_consumer(self):
        request = self.request_factory.get('get-wallet-balance/', format='json')
        request.user = self.user1
        view = get_balance_view
        response = view(request)
        self.assertTrue(response.status_code==status.HTTP_200_OK)
        self.assertTrue(self.consumer.wallet.all()[0].balance==0)

    def test_get_balance_view_with_venue(self):
        request = self.request_factory.get('get-wallet-balance/', format='json')
        request.user = self.user
        view = get_balance_view
        response = view(request)
        self.assertTrue(response.status_code==status.HTTP_200_OK)
        self.assertTrue(self.venue.wallet.all()[0].balance==0)


    def test_load_up_method(self):
        request = self.request_factory.post('load-up/', format='json')
        request.user = self.user1
        view = load_up_money_view
        response = view(request)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(self.consumer.wallet.all()[0].balance == 50)
