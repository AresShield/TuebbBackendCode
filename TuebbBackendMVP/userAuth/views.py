from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LinkVenueToAccountSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import VenueProfile
from .permissions import IsNotLinkedYet


"""
view for account creation
input: first_name, last_name, email, password, password2
output: 201 if successful
"""
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


"""
desc: view to link a venue profile to an account
input: Unique_code as a str (JSON)
output: 202 if successful, 400 otherwise
"""
@api_view(['POST'])
@permission_classes([IsNotLinkedYet, permissions.IsAuthenticated])
def link_account_to_venue(request, format=None):
    # Link a user account to a profile
    if request.method == 'POST':
        venue = VenueProfile.objects.get(unique_code=request.data["unique_code"])
        venue_serializer = LinkVenueToAccountSerializer(venue, data=request.data, context={'request': request})
        if venue_serializer.is_valid():
            venue_serializer.save()
            return Response(venue_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(venue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
desc: check to see if login credentials are valid
requirements: auth credentials
input: -
output: 200 if valid, auth error if not
"""
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def valid_user(request, format=None):
    if request.method == 'POST':
        return Response({"Status": "Valid User!"}, status.HTTP_200_OK)
