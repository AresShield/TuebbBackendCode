from django.contrib.auth import get_user_model
from .serializers import MenuItemSerializer, MenuSerializer, AdvancedProfileVenueSerializer, ChangeTeamMemberSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Menu, MenuItem, AdvancedVenueProfile
from .permissions import IsCreatorOrReadOnlyMenu, IsOwnerOrReadOnlyAdvUserProfile,IsCreatorOrReadOnlyMenuItem
from userAuth.models import VenueProfile


"""
desc: create and change menu items
requirements: auth credentials
for create: use url without primary key parameter and use POST
input: {name:str, description:str, price:float}
output: 201 if valid, 400 if not
for change: use primary key of object as url parameter and use PUT
input: {name, description, price}
output: 200 if valid, 400 if not
"""
@api_view(['POST', "PUT"])
@permission_classes([IsCreatorOrReadOnlyMenuItem, permissions.IsAuthenticated])
def menu_item_view(request, pk=None, format=None):
    if len(VenueProfile.objects.filter(govern_user=request.user)) == 0:
        return Response({"Error":"No valid venue account"}, status=status.HTTP_403_FORBIDDEN)
    if pk and request.method == "PUT":
        item = MenuItem.objects.get(pk=pk)
        """if item.menues.owner.govern_user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)"""
        item_serializer = MenuItemSerializer(item, data=request.data, context={'request': request})
        if item_serializer.is_valid():
            item_serializer.save()
            return Response(item_serializer.data)
    elif request.method == "POST":
        item_serializer = MenuItemSerializer(data=request.data, context={'request': request})
        if item_serializer.is_valid():
            item_serializer.save()
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"supported methods":"PUT,POST"}, status=status.HTTP_400_BAD_REQUEST)



"""
desc: delete menu items and retrieve a menu
requirements: auth credentials
for delete: use url without primary key parameter and use PATCH
input: {delete_menu_items:list of primary ids}
output: 202 if valid, 400 if not
for retrieve: use primary key of object as url parameter 
or none if you want to get your own menu and use GET
input: -
output: 200 if valid, 400 if not, returns list of items on menu
"""
@api_view(['PATCH', "GET"])
@permission_classes([IsCreatorOrReadOnlyMenu, permissions.IsAuthenticated])
def menu_view(request, pk=None, format=None):
    if request.method == "PATCH":
        menu = Menu.objects.get(owner=VenueProfile.objects.get(govern_user=request.user))
        menu_serializer = MenuSerializer(menu, data=request.data, context={'request': request})
        if menu_serializer.is_valid():
            menu_serializer.save()
            return Response(menu_serializer.data, status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        if pk:
            menu = Menu.objects.get(pk=pk)
        elif pk==None and len(VenueProfile.objects.filter(govern_user=request.user))==1:
            menu = Menu.objects.get(owner=VenueProfile.objects.get(govern_user=request.user))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        menu_serializer = MenuSerializer(menu)
        return Response(menu_serializer.data, status=status.HTTP_200_OK)
    return Response({"supported methods":"PATCH,GET"}, status=status.HTTP_400_BAD_REQUEST)


"""
desc: change the profile of a venue and retrieve it
requirements: auth credentials
for change: use url without primary key parameter and use PUT
input: {address:str, opening_hours:str, description:str, contact:str, entry_fee:float, delete_photos:id of image, upload_image: Image to upload}
Note: Only one image can be uploaded at the time
output: 202 if valid, 400 if not
for retrieve: use primary key of object as url parameter or none if you want to get your own profile and use GET
input: -
output: 200 if valid, 400 if not, returns list of items on menu
"""
@api_view(['PUT', "GET"])
@permission_classes([IsOwnerOrReadOnlyAdvUserProfile, permissions.IsAuthenticated])
def adv_venue_profile_view(request, pk=None, format=None):
    if request.method == "PUT":
        if len(VenueProfile.objects.filter(govern_user=request.user)) == 0:
            return Response(status=status.HTTP_403_FORBIDDEN)
        adv_profile = AdvancedVenueProfile.objects.get(venue_profile=VenueProfile.objects.get(govern_user=request.user))
        adv_profile_serializer = AdvancedProfileVenueSerializer(adv_profile, data=request.data, context={'request': request})
        if adv_profile_serializer.is_valid():
            adv_profile_serializer.save()
            return Response(adv_profile_serializer.data, status.HTTP_202_ACCEPTED)
        else:
            return Response({"Error": "validation error"},status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        if pk:
            adv_profile = AdvancedVenueProfile.objects.get(pk=pk)
        elif pk==None and len(VenueProfile.objects.filter(govern_user=request.user))==1:
            adv_profile = AdvancedVenueProfile.objects.get(venue_profile=VenueProfile.objects.get(govern_user=request.user))
        else:
            return Response({"Error": "No Venue found with your criteria"},status=status.HTTP_400_BAD_REQUEST)
        adv_profile_serializer = AdvancedProfileVenueSerializer(adv_profile)
        data = adv_profile_serializer.data
        if pk==None:
            team_members = ChangeTeamMemberSerializer(adv_profile)
            data["team"] = team_members.data
        return Response(data, status=status.HTTP_200_OK)
    return Response({"supported methods":"PUT,GET"}, status=status.HTTP_400_BAD_REQUEST)


"""
desc: add and remove team members to a venue admin profile
requirements: auth credentials
use PATCH
input: {remove_team_member:str (email of a user), add_team_member:str (email of a user)}
Note: Only one remove and add per day
output: 202 if valid, 400 if not, outputs all the current team members
"""
@api_view(['PATCH'])
@permission_classes([IsOwnerOrReadOnlyAdvUserProfile, permissions.IsAuthenticated])
def change_team_members_view(request, format=None):
    if request.method == "PATCH":
        if len(VenueProfile.objects.filter(govern_user=request.user)) == 0:
            return Response(status=status.HTTP_403_FORBIDDEN)
        adv_profile = AdvancedVenueProfile.objects.get(venue_profile=VenueProfile.objects.get(govern_user=request.user))
        change_team_member_seri = ChangeTeamMemberSerializer(adv_profile, data=request.data, context={'request': request})
        if change_team_member_seri.is_valid():
            change_team_member_seri.save()
            return Response(change_team_member_seri.data, status.HTTP_202_ACCEPTED)
        else:
            return Response({"Error": "validation error"},status=status.HTTP_400_BAD_REQUEST)
    return Response({"supported methods":"PATCH"}, status=status.HTTP_400_BAD_REQUEST)
