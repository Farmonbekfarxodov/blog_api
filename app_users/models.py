import random
import string


from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from app_common.models import BaseModel
from django.core.exceptions import ValidationError





class ProfileModels(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile")
    avatar = models.ImageField(upload_to="profiles",null=True,
                               validators=[FileExtensionValidator(allowed_extensions=['png','jpg','gif'])])
    short_bio = models.CharField(max_length=160,null=True)
    about = models.TextField(null=True)
    pronouns = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)  
    verification_code = models.CharField(max_length=6, blank=True, null=True)  
    last_activity = models.DateTimeField(blank=True, null=True)

    def generate_verification_code(self):
        """6 xonali tasodifiy kod yaratish"""
        self.verification_code = ''.join(random.choices(string.digits, k=6))
        self.save()



class FollowModel(BaseModel):  # `BaseModel` noto‘g‘ri bo‘lsa, `models.Model` ishlatamiz
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following'
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers'
    )

    def __str__(self):
        return f"{self.from_user.username} following {self.to_user.username}"

    def clean(self):
        """O‘zini o‘zi follow qilishni taqiqlaymiz."""
        if self.from_user == self.to_user:
            raise ValidationError("You cannot follow yourself.")

    class Meta:
        verbose_name = "follower"
        verbose_name_plural = "followers"
        unique_together = ('from_user', 'to_user')  # Takroriy follow qilishni oldini oladi
        constraints = [
            models.CheckConstraint(
                check=~models.Q(from_user=models.F('to_user')),
                name='prevent_self_follow'
            )
        ]

