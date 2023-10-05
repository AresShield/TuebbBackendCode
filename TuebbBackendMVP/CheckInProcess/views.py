from django.shortcuts import render
from .serializers import TicketCreationSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .permissions import TicketPermissions

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
