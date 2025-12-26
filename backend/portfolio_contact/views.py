from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
def contact_api(request):
    return Response(
        {
            "success": True,
            "data": request.data,
            "message": "Contact API working on Render 🚀"
        },
        status=status.HTTP_200_OK
    )
