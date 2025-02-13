from django.contrib.auth.models import User
from rest_framework import serializers

from app_posts.models import PostsModel



class PostsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    title = serializers.CharField()
    body = serializers.CharField(allow_blank=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    created_at = serializers.DateTimeField(read_only=True)

    def create(self,validated_data):
        return PostsModel.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        instance.title = validated_data.get('title')
        instance.body = validated_data.get('body')
        instance.author = validated_data.get('author')
        instance.save()
        return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["extra"] = "qo'shildi"
        return data
    
    def validate(self,attrs):
        print(attrs)
        return attrs
    
    def validate_title(self,value):
        print(value)
        raise serializers.ValidationError({"error":"test"})     

   
