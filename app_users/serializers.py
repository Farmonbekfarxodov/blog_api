from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import generate_verification_code, send_verification_email

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        # Tasdiqlash kodini generatsiya qilish
        verification_code = generate_verification_code()
        user.verification_code = verification_code
        user.email_verified = False
        user.save(update_fields=['verification_code', 'email_verified'])

        # Emailga kodni jo‘natish
        send_verification_email(user.email, verification_code)
        
        return user

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Login qilishdan oldin email tasdiqlanganligini tekshirish"""
    def validate(self, attrs):
        data = super().validate(attrs)

        if not hasattr(self, 'user') or not self.user.email_verified:
            raise serializers.ValidationError("Email tasdiqlanmagan!")

        return data
