from django.urls import path

# views
from users.views import UserView


urlpatterns = [
    path("register/", UserView.register, name="user-register"),
    path(
        "verify-email/<int:id>/<str:token>/",
        UserView.verify_email,
        name="verify-user-email",
    ),
    path("user-details/", UserView.get_user_data, name="user-data"),
    path("login/", UserView.login, name="user-login"),
    path("logout/", UserView.logout, name="user-logout"),
    path("forgot-password/", UserView.forgot_password, name="forgot-password"),
    path("reset-password/<str:token>/", UserView.reset_password, name="reset-password"),
    path("change-password/", UserView.change_password, name="change-password"),
    path(
        "change-phone-number/", UserView.change_phone_number, name="change-phone-number"
    ),
    path("change-location/", UserView.change_location, name="change-location"),
    path("change-names/", UserView.change_names, name="change-names"),
    path(
        "change-profile-picture/",
        UserView.change_profile_picture,
        name="change-profile-picture",
    ),
]
