from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterView, VerifyEmailView, CustomTokenObtainPairView, CheckInactivityView


app_name = "users"

urlpatterns = [
  
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('check-inactivity/', CheckInactivityView.as_view(), name='check-inactivity'),
]
