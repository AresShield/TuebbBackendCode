from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import consumer_account_creation_view, ConsumerProfileView
from rest_framework.test import force_authenticate
from .models import ConsumerUser


class MenuAndMenuItemTesting(TestCase):
    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email='javed@javed.com', password='my_secret')
        self.user1 = get_user_model().objects.create_user(
            email='bert@bert.com', password='my_secret')
        self.consumer = ConsumerUser.objects.create(user=self.user1, age=50, gender="Male")

    def test_consumer_account_creation(self):
        request = self.request_factory.post('/consumer-account-creation/', format='json')
        request.user = self.user
        view = consumer_account_creation_view
        response = view(request)
        self.assertTrue(response.status_code==status.HTTP_201_CREATED)
        self.assertTrue(self.user.consumer_account)

    def test_changing_age(self):
        obj = {
            "age": 40,
        }
        request = self.request_factory.patch('/consumer-account-updates/', obj, format='json')
        request.user = self.user1
        view = ConsumerProfileView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(self.user1.consumer_account.all()[0].age==40)


    def test_retrieving_information(self):
        request = self.request_factory.get('/consumer-account-updates/', format='json')
        request.user = self.user1
        view = ConsumerProfileView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(response.data["age"] == 50)
