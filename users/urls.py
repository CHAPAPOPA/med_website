from django.urls import path

from .apps import UsersConfig
from .views import (RegisterView, UserConfirmationFailView,
                    UserConfirmationSentView, UserConfirmedView,
                    UserConfirmEmailView, UserDetailView, UserLogin,
                    UserLogout, UserUpdateView, generate_new_password,
                    regenerate_password, users)

app_name = UsersConfig.name

urlpatterns = [
    path("users", users),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", UserLogout.as_view(next_page="main:index"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "confirm_email/<str:uidb64>/<str:token>/",
        UserConfirmEmailView.as_view(),
        name="confirm_email",
    ),
    path("email_confirmed/", UserConfirmedView.as_view(), name="email_confirmed"),
    path(
        "email_confirmation_failed/",
        UserConfirmationFailView.as_view(),
        name="email_confirmation_failed",
    ),
    path("profile/genpassword/", generate_new_password, name="generate_new_password"),
    path("regenerations/", regenerate_password, name="regenerate_password"),
    path(
        "email_confirmation_sent/",
        UserConfirmationSentView.as_view(),
        name="email_confirmation_sent",
    ),
    path("profile/update/", UserUpdateView.as_view(), name="profile_update"),
    path("profile/", UserDetailView.as_view(), name="profile"),
]
