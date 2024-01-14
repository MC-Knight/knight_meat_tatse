from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.forms import UserCreationForm, UserChangeForm
from .models import User

admin.site.site_header = "Mentor Administration"


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
        "first_name",
        "last_name",
        "user_type",
        "is_verfied",
        "is_active",
    )
    list_filter = (
        "email",
        "user_type",
        "is_staff",
        "is_verfied",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email_token",
                    "is_verfied",
                    "phone_number",
                    "address_1",
                    "address_2",
                    "city",
                    "country",
                    "profile_picture",
                )
            },
        ),
        ("Permissions", {"fields": ("user_type", "is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "user_type",
                    "is_staff",
                    "is_active",
                    "is_verfied",
                    "phone_number",
                    "address_1",
                    "address_2",
                    "city",
                    "country",
                    "profile_picture",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, UserAdmin)
