from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models



class ProfileModels(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
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
