# drf yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# django
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

# restframework
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
    parser_classes,
)
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser


from rest_api.models import Dish

from rest_api.serializers import DishSerializer

User = get_user_model()


class UserView:
    """
    in this class there are all views for dish CRUD entities
    """

    @swagger_auto_schema(
        method="POST",
        tags=["Auth"],
        request_body=DishSerializer,
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer {token}",
            ),
        ],
    )
    @api_view(["POST"])
    @permission_classes((IsAuthenticated,))
    def create_dist(request):
        user = request.user
        data = request.data

        serializer = DishSerializer(data=data, context={"request": request})

        pass
