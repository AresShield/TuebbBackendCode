from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import ticket_creation_view
from rest_framework.test import force_authenticate
from .models import Ticket
from userAuth.models import VenueProfile
import tempfile
from PIL import Image as ImageFile
from VenueAdmins.models import AdvancedVenueProfile

# Create your tests here.
class TicketTests(TestCase):
    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email='javed@javed.com', password='my_secret')
        self.user1 = get_user_model().objects.create_user(
            email='bert@bert.com', password='my_secret')
        self.user2 = get_user_model().objects.create_user(
            email='anna@anna.com', password='my_secret')
        self.venue = VenueProfile.objects.create(company_name="ExampleVenue", unique_code="12345", govern_user=self.user)
        self.adv_profile1 = AdvancedVenueProfile.objects.create(venue_profile=self.venue, entry_fee=15)
        self.adv_profile1.team.add(self.user1)
        self.adv_profile1.save()

    def test_creating_tickets(self):
        request = self.request_factory.post('/ticket-creation/', format='json')
        request.user = self.user1
        view = ticket_creation_view
        response = view(request)
        self.assertTrue(response.status_code==status.HTTP_201_CREATED)
        self.assertTrue(len(Ticket.objects.filter(creator=self.adv_profile1))==1)

    def test_creating_tickets_invalid_permission(self):
        request = self.request_factory.post('/ticket-creation/', format='json')
        request.user = self.user2
        view = ticket_creation_view
        response = view(request)
        self.assertTrue(response.status_code==status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(Ticket.objects.filter(creator=self.adv_profile1))==0)
