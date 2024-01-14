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

# restframework_simplejwt
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


# uuid to be used where needed
import uuid

from users.serializers import (
    RegisterUserSerializer,
    UserSerializer,
    ResetPasswordSerializer,
    ForgotPasswordSerializer,
    ChangePasswordSerializer,
    PhoneNumberSerializer,
    UserLocationSerializer,
    UserChangeNamesSerializer,
    ChangeProfilePictureSerializer,
)

# utilities module
from users.utils import send_verification_email, send_reset_password_email


User = get_user_model()


class UserView:
    """
    in this class there is all views for user basic actions including Registration, Login, EmailVerfication
    Reset Forgotten Password, Change Password and CRUD to User profile picture
    """

    @swagger_auto_schema(
        method="POST", tags=["Auth"], request_body=RegisterUserSerializer
    )
    @api_view(["POST"])
    def register(request):
        """
        user registration
        """
        serializer = RegisterUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            email_verification_token = uuid.uuid4()
            user_id = user.id

            user.email_token = email_verification_token
            user.save()

            send_verification_email(user.email, user_id, email_verification_token)

            return Response(
                {
                    "message": "account created successfully. Check your email to verify your account.",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="POST",
        tags=["Auth"],
    )
    @api_view(["POST"])
    def verify_email(request, id, token):
        """
        Verifying user email
        """
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(
                {"message": "User Not Found Try Again or resend verfication email."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.is_verfied:
            return Response(
                {"message": "Email already verified."}, status=status.HTTP_200_OK
            )

        if user.email_token == token:
            user.is_verfied = True
            user.email_token = None
            user.save()

            return Response(
                {"message": "Email verified successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "message": "Invalid or expired token try to resend verification email."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        method="GET",
        tags=["Auth"],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer {token}",
            ),
        ],
    )
    @api_view(["GET"])
    @permission_classes((IsAuthenticated,))
    def get_user_data(request):
        """
        Getting current loggedin users data
        """
        serializer = UserSerializer(request.user, context={"request": request})
        user = serializer.data

        return Response(
            {
                "user": {
                    "id": user["id"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "email": user["email"],
                    "phone_number": user["phone_number"],
                    "address_1": user["address_1"],
                    "address_2": user["address_2"],
                    "city": user["city"],
                    "country": user["country"],
                    "profile_picture": user["profile_picture"],
                    "type": user["user_type_display"],
                }
            }
        )

    @swagger_auto_schema(
        method="POST",
        tags=["Auth"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD
                ),
            },
        ),
    )
    @api_view(["POST"])
    def login(request):
        """
        Loggin in User and Authenticating with simplejwt
        """

        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"message": "Both email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "User with that email doesn't exist."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_verfied:
            return Response(
                {
                    "message": "Please Acticate your account first, check your email inbox."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.check_password(password):
            serializer = UserSerializer(user, context={"request": request})
            logged_user = serializer.data
            # Authentication successful, generate tokens
            refresh = RefreshToken.for_user(user)
            data = {
                "message": "Logged In successfully",
                "user": {
                    "id": logged_user["id"],
                    "first_name": logged_user["first_name"],
                    "last_name": logged_user["last_name"],
                    "email": logged_user["email"],
                    "phone_number": logged_user["phone_number"],
                    "address_1": logged_user["address_1"],
                    "address_2": logged_user["address_2"],
                    "city": logged_user["city"],
                    "country": logged_user["country"],
                    "profile_picture": logged_user["profile_picture"],
                },
                "access": str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "wrong email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @swagger_auto_schema(
        method="POST",
        tags=["Auth"],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer {token}",
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING,
                ),
            },
        ),
    )
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def logout(request):
        """
        Logout User
        """
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"message": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            RefreshToken(refresh_token).blacklist()
            return Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_200_OK,
            )
        except TokenError:
            return Response(
                {"message": "Invalid refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        method="POST",
        tags=["Auth"],
        request_body=ForgotPasswordSerializer,
    )
    @api_view(["POST"])
    def forgot_password(request):
        """
        Send Email for changing Forgotten Password
        """
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "User with this email does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.password_reset_token = get_random_string(length=32)
        user.save()

        send_reset_password_email(user.email, user.password_reset_token)

        return Response(
            {
                "message": "An email has been sent to your email address. Please check your email to reset your password."
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        method="POST", tags=["Auth"], request_body=ResetPasswordSerializer
    )
    @api_view(["POST"])
    def reset_password(request, token):
        """
        reset password view
        """
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data["password1"]

        try:
            user = User.objects.get(
                password_reset_token=token,
            )
        except User.DoesNotExist:
            return Response(
                {"message": "something goes wrong try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(password)
        user.password_reset_token = None
        user.save()

        return Response(
            {"message": "Password reset successful."},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        method="POST",
        tags=["Auth"],
        request_body=ChangePasswordSerializer,
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
    def change_password(request):
        user = request.user
        data = request.data
        serializer = ResetPasswordSerializer(data=data, context={"request": request})

        if serializer.is_valid():
            if not user.check_password(data["old_password"]):
                return Response(
                    {"message": "Incorrect old password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(serializer.validated_data["password1"])
            user.save()
            return Response(
                {"message": "Password changed successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="PATCH",
        tags=["User"],
        request_body=PhoneNumberSerializer,
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer {token}",
            ),
        ],
    )
    @api_view(["PATCH"])
    @permission_classes((IsAuthenticated,))
    def change_phone_number(request):
        user = request.user
        data = request.data
        serializer = PhoneNumberSerializer(data=data)

        if serializer.is_valid():
            user.phone_number = serializer.validated_data["phone_number"]
            user.save()
            return Response(
                {"message": "Phone number Updated successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Phone number Failed To be updated"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        method="PUT",
        tags=["User"],
        request_body=UserLocationSerializer,
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer {token}",
            ),
        ],
    )
    @api_view(["PUT"])
    @permission_classes((IsAuthenticated,))
    def change_location(request):
        user = request.user
        data = request.data
        serializer = UserLocationSerializer(data=data)

        if serializer.is_valid():
            user.address_1 = serializer.validated_data["address_1"]
            user.address_2 = serializer.validated_data["address_2"]
            user.city = serializer.validated_data["city"]
            user.country = serializer.validated_data["country"]
            user.save()
            return Response(
                {"message": "Location Updated successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Location Failed To be updated."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        method="PUT",
        tags=["User"],
        request_body=UserChangeNamesSerializer,
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer {token}",
            ),
        ],
    )
    @api_view(["PUT"])
    @permission_classes((IsAuthenticated,))
    def change_names(request):
        user = request.user
        data = request.data
        serializer = UserChangeNamesSerializer(data=data)

        if serializer.is_valid():
            user.first_name = serializer.validated_data["first_name"]
            user.last_name = serializer.validated_data["last_name"]
            user.save()
            return Response(
                {"message": "Names Updated successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Names Failed To be updated."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        method="PUT",
        tags=["User"],
        request_body=ChangeProfilePictureSerializer,
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer {token}",
            ),
        ],
    )
    @api_view(["PUT"])
    @permission_classes((IsAuthenticated,))
    def change_profile_picture(request):
        user = request.user
        data = request.data
        serializer = ChangeProfilePictureSerializer(data=data)

        if serializer.is_valid():
            user.profile_picture = serializer.validated_data["profile_picture"]
            user.save()
            return Response(
                {
                    "message": "Profile Picture Updated successfully, it may take minute to appear here reload to see changes."
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Profile Picture Failed To be updated."},
            status=status.HTTP_400_BAD_REQUEST,
        )
