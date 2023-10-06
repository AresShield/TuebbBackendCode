from django.shortcuts import render
from .serializers import TicketCreationSerializer, TicketSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .permissions import TicketPermissions, TicketReadPermissions, TicketBuyPermissions
from rest_framework import generics
from .models import Ticket
from .payment_handling import check_if_enough_funds, buy_ticket

# Create your views here.
@api_view(['POST'])
@permission_classes([TicketPermissions, permissions.IsAuthenticated])
def ticket_creation_view(request, format=None):
    if request.method == "POST":
        ticket_serializer = TicketCreationSerializer(data=request.data, context={'request': request})
        if ticket_serializer.is_valid():
            ticket_serializer.save()
            return Response(ticket_serializer.data, status=status.HTTP_201_CREATED)
        return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"supported methods":"POST"}, status=status.HTTP_400_BAD_REQUEST)


class TicketInfoView(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    permissions = [TicketReadPermissions, permissions.IsAuthenticated]
    queryset = Ticket.objects.all()


@api_view(['PATCH'])
@permission_classes([TicketBuyPermissions, permissions.IsAuthenticated])
def buy_ticket_view(request, pk=None,format=None):
    if request.method == "PATCH" and pk:
        ticket = Ticket.objects.get(pk=pk)
        consumer_wallet = request.user.consumer_account.all()[0].wallet.all()[0]
        venue_wallet = ticket.creator.venue_profile.wallet.all()[0]
        if not check_if_enough_funds(ticket, consumer_wallet):
            return Response({"Error": "Not enough funds"}, status=status.HTTP_400_BAD_REQUEST)
        buy_ticket(ticket, consumer_wallet, venue_wallet, request.user)
        ticket_seri = TicketSerializer(ticket)
        return Response(ticket_seri.data, status=status.HTTP_200_OK)
    return Response({"Error":"No ticket specified"}, status=status.HTTP_400_BAD_REQUEST)
