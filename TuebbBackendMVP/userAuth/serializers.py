from rest_framework import serializers
from .models import CustomUser, VenueProfile
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



# account creation serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user



# Serializer to link Venue Profile to User account
class LinkVenueToAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = VenueProfile
        fields = ('unique_code', 'govern_user')

    def validate(self, attrs):
        venue = VenueProfile.objects.get(unique_code=attrs['unique_code'])
        if venue.govern_user:
            raise serializers.ValidationError({"unique_code": "Unique code already has been used!"})
        return attrs

    def update(self, instance, validated_data):
        instance.govern_user = self.context['request'].user
        instance.save()
        return instance
