from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings


@api_view(["POST"])
def contact_api(request):
    name = request.data.get("name")
    email = request.data.get("email")
    message = request.data.get("message")

    if not name or not email or not message:
        return Response(
            {"error": "All fields are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🔥 EMAIL SHOULD NEVER BREAK API
    try:
        send_mail(
            subject=f"Portfolio Message from {name}",
            message=f"From: {email}\n\nMessage:\n{message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=True,   # 🔑 KEY
        )
    except Exception as e:
        print("Email error (ignored):", e)

    return Response(
        {"success": "Message sent successfully"},
        status=status.HTTP_200_OK
    )
