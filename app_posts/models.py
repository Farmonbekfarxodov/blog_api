from django.db import models
from django.conf import settings


from app_common.models import BaseModel


class TopicsModel(BaseModel):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "topic"
        verbose_name_plural = "topics"

class PostsModel(BaseModel):
    image = models.ImageField(upload_to="posts",null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="posts")
    title = models.CharField(max_length=255)
    slug =  models.SlugField(unique=True,blank=True)
    short_description =  models.CharField(max_length=255)
    body = models.TextField()

    topics = models.ManyToManyField(TopicsModel,related_name="posts")
    

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
    




class PostClapsModel(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,
                             related_name = "post_claps",null=True
                            )
    post = models.ForeignKey(
        PostsModel,on_delete=models.CASCADE,related_name="claps"

    )

    def __str__(self):
        return f"{self.post.id} clapped by {self.user.username}"
    class Meta:
        verbose_name = "post clap"
        verbose_name_plural = "post claps"

class PostCommentModel(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,
        related_name="post_comments",null=True
    )
    post = models.ForeignKey(
        PostsModel,on_delete=models.CASCADE,related_name="comments"
    )

    comment = models.TextField()
    parent = models.ForeignKey('self',on_delete=models.CASCADE,related_name="children")

    def __str__(self):
        return f"{self.user.username} comment to {self.post.id} like:{self.comment}"
    
    class Meta:
        verbose_name = "post comment"
        verbose_name_plural = "post comments"

class PostCommentClapsModel(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,
        related_name="post_comments_claps",null=True
    )
    comment = models.ForeignKey(
        PostCommentModel,on_delete=models.CASCADE,related_name="claps"
    )

    def __str__(self):
        return f"{self.comment.id} clopped by {self.user.username}"
    
    class Meta:
        verbose_name = "post comment clap"
        verbose_name_plural ="post comment claps"

    

