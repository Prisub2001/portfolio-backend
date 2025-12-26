import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

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

    try:
        requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": "Portfolio <onboarding@resend.dev>",
                "to": ["yourgmail@gmail.com"],
                "subject": f"Portfolio Message from {name}",
                "html": f"""
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p>{message}</p>
                """,
            },
            timeout=5,   # 🔥 HARD LIMIT
        )
    except Exception as e:
        print("Email API error:", e)

    return Response(
        {"success": "Message sent successfully"},
        status=status.HTTP_200_OK
    )
