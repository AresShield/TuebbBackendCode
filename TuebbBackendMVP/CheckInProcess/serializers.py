from .models import Ticket
from rest_framework import serializers

class TicketCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id",]

    def create(self, validated_data):
        user = self.context["request"].user
        adv_venue = user.venue.all()[0]
        ticket = Ticket.objects.create(creator=adv_venue, price=adv_venue.entry_fee, paid=False)
        return ticket

class TicketSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="creator.venue_profile.company_name")
    #first_name = serializers.CharField(source="owner.first_name")
    #last_name = serializers.CharField(source="owner.last_name")

    class Meta:
        model = Ticket
        fields = ["id", "company_name", "price", "paid"]
