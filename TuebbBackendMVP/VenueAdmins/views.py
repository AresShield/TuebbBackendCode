from django.contrib.auth import get_user_model
from .serializers import MenuItemSerializer, MenuSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Menu, MenuItem
from .permissions import IsCreatorOrReadOnlyMenu, IsCreatorOrReadOnlyMenuItem
from userAuth.models import VenueProfile



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

