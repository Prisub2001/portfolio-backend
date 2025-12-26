from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from .serializers import ContactSerializer

@api_view(['POST'])
def contact_api(request):
    serializer = ContactSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        message = serializer.validated_data['message']

        send_mail(
            subject=f'Portfolio Message from {name}',
            message=f'Email: {email}\n\nMessage:\n{message}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
        )

        return Response(
            {'success': 'Message sent successfully'},
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
