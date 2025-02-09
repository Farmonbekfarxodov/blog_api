from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugity

from app_posts.models import PostsModel

 
@receiver(pre_save,sender=PostsModel)
def generate_slug_for_post(sender,instance,**kwargs):
    original_slug = slugity(instance.title)
    slug = original_slug
    count = 0
    while PostsModel.objects.filter(slug=slug).exists():
        slug = f"{original_slug}.{count}"
        count += 1
    
    instance.slug = slug