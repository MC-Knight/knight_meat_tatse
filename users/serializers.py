from rest_framework import serializers, validators
from django.contrib.auth.password_validation import validate_password
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    user_type_display = serializers.ChoiceField(
        choices=User.USER_TYPE_CHOICES, source="get_user_type_display", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "user_type_display",
            "phone_number",
            "address_1",
            "address_2",
            "city",
            "country",
            "profile_picture",
        )


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")
        extra_kwarg = {
            "first_name": {
                "required": True,
                "allow_blank": False,
            },
            "last_name": {
                "required": True,
                "allow_blank": False,
            },
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(),
                        "Account with that Email already exists",
                    )
                ],
            },
        }

    def validate(self, attrs):
        """
        Custom validation for password fields.
        """
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        """
        Create and return a new user instance.
        """
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        email = validated_data.get("email")

        user = User.objects.create(
            first_name=first_name, last_name=last_name, email=email
        )

        user.set_password(validated_data["password1"])
        user.save()

        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["password1", "password2"]

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password1", "password2")

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone_number",)


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("address_1", "address_2", "city", "country")


class UserChangeNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )


class ChangeProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("profile_picture",)
