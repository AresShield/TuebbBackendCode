from django.shortcuts import render
from .serializers import CreateConsumerAccountForUserSerializer, ConsumerAccountSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .permissions import HasPermissionToCreateAccount, IsCreator
from rest_framework import generics
from .models import ConsumerUser
from django.shortcuts import get_object_or_404


# Create your views here.
@api_view(['POST'])
@permission_classes([HasPermissionToCreateAccount, permissions.IsAuthenticated])
def consumer_account_creation_view(request, format=None):
    if request.method == "POST":
        consumer_serializer = CreateConsumerAccountForUserSerializer(data=request.data, context={'request': request})
        if consumer_serializer.is_valid():
            consumer_serializer.save()
            return Response(consumer_serializer.data, status=status.HTTP_201_CREATED)
        return Response(consumer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"supported methods":"POST"}, status=status.HTTP_400_BAD_REQUEST)


class ConsumerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ConsumerAccountSerializer
    permissions = [IsCreator, permissions.IsAuthenticated]
    queryset = ConsumerUser.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
