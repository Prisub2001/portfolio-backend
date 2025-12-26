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
        instance = serializer.save()

        # 🔥 EMAIL SHOULD NEVER BREAK API
        try:
            send_mail(
                subject=f"Portfolio Message from {instance.name}",
                message=f"Email: {instance.email}\n\nMessage:\n{instance.message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=True,   # ✅ KEY FIX
            )
        except Exception as e:
            print("Email error (ignored):", e)

        return Response(
            {"success": "Message received successfully"},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
