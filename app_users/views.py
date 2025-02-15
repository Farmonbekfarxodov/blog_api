from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, VerifyEmailSerializer, CustomTokenObtainPairSerializer
from .utils import generate_verification_code, send_verification_email

User = get_user_model()

class RegisterView(APIView):
    """Foydalanuvchini ro‘yxatdan o‘tkazish"""
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            
            verification_code = generate_verification_code()
            user.verification_code = verification_code
            user.email_verified = False
            user.save(update_fields=['verification_code', 'email_verified'])

            send_verification_email(user.email, verification_code)

            return Response({"message": "Emailga tasdiqlash kodi yuborildi!"}, status=201)
        return Response(serializer.errors, status=400)

class VerifyEmailView(APIView):
    """Emailni tasdiqlash"""
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            try:
                user = User.objects.get(email=email)
                if user.verification_code == code:
                    user.email_verified = True
                    user.verification_code = None
                    user.save(update_fields=['email_verified', 'verification_code'])
                    return Response({"message": "Email muvaffaqiyatli tasdiqlandi!"}, status=200)
                return Response({"error": "Tasdiqlash kodi noto‘g‘ri"}, status=400)
            except User.DoesNotExist:
                return Response({"error": "Bunday foydalanuvchi topilmadi!"}, status=404)
        return Response(serializer.errors, status=400)

class CustomTokenObtainPairView(TokenObtainPairView):
    """Foydalanuvchi login qilish"""
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        try:
            user = User.objects.get(username=request.data.get("username") or request.data.get("email"))
            if not user.email_verified:
                return Response({"error": "Email tasdiqlanmagan!"}, status=400)
        except User.DoesNotExist:
            return Response({"error": "Bunday foydalanuvchi topilmadi!"}, status=404)
        return response

class CheckInactivityView(APIView):
    """10 daqiqa inaktiv bo‘lsa, foydalanuvchini logout qilish"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.last_activity and now() - user.last_activity > timedelta(minutes=10):
            return Response({"message": "Sizning sessiyangiz tugadi. Qayta login qiling."}, status=401)
        
        
        user.last_activity = now()
        user.save(update_fields=['last_activity'])
        return Response({"message": "Foydalanuvchi hali faol"}, status=200)
