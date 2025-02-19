from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

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
class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True, write_only=True) 

    def validate_old_password(self, value):
        """Eski parol foydalanuvchining hozirgi paroliga mosligini tekshiradi."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Eski parol noto‘g‘ri.")
        return value

    def validate(self, attrs):
        """Yangi parol va tasdiqlash paroli mos kelishini tekshiradi."""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Parollar mos kelmadi."})
        return attrs

    def update_password(self):
        """Foydalanuvchining parolini yangilaydi."""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Email ro‘yxatdan o‘tganligini tekshirish"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email tizimda mavjud emas.")
        return value

    def send_reset_code(self):
        """Emailga parolni tiklash kodini yuborish"""
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        
        # Tasdiqlash kodini generatsiya qilish
        reset_code = generate_verification_code()
        user.verification_code = reset_code
        user.save(update_fields=['verification_code'])

        # Emailga kodni jo‘natish
        send_verification_email(user.email, reset_code)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Email va kodni tekshirish"""
        email = attrs.get('email')
        code = attrs.get('code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Bu email tizimda mavjud emas."})

        if user.verification_code != code:
            raise serializers.ValidationError({"code": "Kod noto‘g‘ri yoki eskirgan."})

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Parollar mos kelmadi."})

        return attrs

    def reset_password(self):
        """Yangi parolni saqlash"""
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['new_password'])
        user.verification_code = None  # Kodni o‘chiramiz
        user.save()