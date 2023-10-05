from .models import ConsumerUser
from rest_framework import serializers

class CreateConsumerAccountForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerUser
        fields = []

    def create(self, validated_data):
        user = self.context["request"].user
        consumer = ConsumerUser.objects.create(user=user)
        return consumer


class ConsumerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerUser
        fields = ["age", "gender"]
