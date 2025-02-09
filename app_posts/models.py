from django.db import models
from django.contrib.auth.models import User


class PostsModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="posts")
    title = models.CharField(max_length=255)
    slug =  models.SlugField(unique=True,blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    

