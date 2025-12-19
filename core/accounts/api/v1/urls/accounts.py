from django.urls import path, include
from .. import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    # Registration
    path("registration/", views.RegistrationApiView.as_view(), name="registration"),
    # path('test/email', views.TestEmailSend.as_view(), name='test/email'),
    # Activision
    path(
        "activation/confirm/<str:token>",
        views.ActivationApiView.as_view(),
        name="activation",
    ),
    # Resend Activision
    path(
        "activation/resend/",
        views.ActivationResendApiView.as_view(),
        name="activision-resend",
    ),
    # Password Changing
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # Password reset
    path(
        "password-reset/",
        views.PasswordResetRequestApiView.as_view(),
        name="password-reset",
    ),
    path(
        "password-reset/confirm/<str:token>/",
        views.SetNewPasswordApiView.as_view(),
        name="password-reset-confirm",
    ),
    # Login Token
    path("token/login", views.CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout", views.CustomDiscardAuthToken.as_view(), name="token-logout"),
    # JWT Login
    path("jwt/create", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
