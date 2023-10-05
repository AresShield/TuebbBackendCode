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
