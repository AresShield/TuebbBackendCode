from django.shortcuts import render
from .serializers import VenueAccountWalletSerializer, ConsumerAccountWalletSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import VenueWallet, ConsumerWallet
from django.shortcuts import get_object_or_404



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_balance_view(request, format=None):
    if len(request.user.venue_profile.all()) > 0:
        profile = request.user.venue_profile.all()[0]
        wallet = VenueWallet.objects.get(owner=profile)
        wallet_seri = VenueAccountWalletSerializer(wallet, context={'request': request})
        return Response(wallet_seri.data, status=status.HTTP_200_OK)
    elif len(request.user.consumer_account.all()) > 0:
        profile = request.user.consumer_account.all()[0]
        wallet = profile.wallet.all()[0]
        wallet_seri = ConsumerAccountWalletSerializer(wallet, context={'request': request})
        return Response(wallet_seri.data, status=status.HTTP_200_OK)
    else:
        return Response({"Error": "no valid account"}, status=status.HTTP_400_BAD_REQUEST)



# JUST FOR TESTING PURPOSES!
# DON'T USE IN PRODUCTION OBVIOUSLY
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def load_up_money_view(request, format=None):
    profile = request.user.consumer_account.all()[0]
    wallet = profile.wallet.all()[0]
    wallet.balance += 50.0
    wallet.save()
    return Response({"Balance": wallet.balance}, status=status.HTTP_200_OK)
