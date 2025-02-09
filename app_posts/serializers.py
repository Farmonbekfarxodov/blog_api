from rest_framework import serializers

from app_posts.models import PostsModel


class PostSerialazir(serializers.ModelSerializer):
    class Meta:
        model = PostsModel
        fields = '__all__'