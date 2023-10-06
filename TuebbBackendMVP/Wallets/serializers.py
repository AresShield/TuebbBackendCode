from .models import VenueWallet, ConsumerWallet
from rest_framework import serializers



class WalletSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        user = self.context["request"].user
        data = self.context["request"].data

        if data.get("remove"):
            instance.balance -= data.get("remove")
        if data.get("add"):
            instance.balance += data.get("add")

        instance.save()



class VenueAccountWalletSerializer(WalletSerializer):
    class Meta:
        model = VenueWallet
        fields = ["balance",]

class ConsumerAccountWalletSerializer(WalletSerializer):
    class Meta:
        model = ConsumerWallet
        fields = ["balance",]
