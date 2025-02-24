from rest_framework import serializers

from app_posts.models import  PostCommentModel, PostsModel, TopicsModel
from app_users.views import User

class PostAuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.ImageField(source="profile.avatar",read_only=True)
    
    class Meta:
        model = User
        fields = ['full_name','avatar']
    
    @staticmethod
    def get_full_name(obj):
        return obj.get_full_name()
    

class PostSerializer(serializers.ModelSerializer):
    topics = serializers.PrimaryKeyRelatedField(
        queryset = TopicsModel.objects.all(),
        many=True,
        required = False,
        write_only=True
    )
    comments_count =  serializers.SerializerMethodField()
    claps_count = serializers.SerializerMethodField()

    class Meta:
        model  = PostsModel
        fields = ['slug','image','title','body','short_description',
                  'comments_count','claps_count','topics','created_at']
        read_only_fileds = ['created_at','slug']

    @staticmethod
    def get_claps_count(obj):
        return obj.claps.count()
    
    @staticmethod
    def get_comments_count(obj):
        return obj.comments.count()
    
    def to_representation(self,instance):
        data = super().to_representation(instance)
        data['author'] = PostAuthorSerializer(instance=instance.author).data
        
        return data
    
class PostClapsSerializer(serializers.Serializer):
    slug = serializers.SlugField()


    def validate(self,attrs):
        slug = attrs.get('slug')

        try:
            post = PostsModel.objects.get(slug=slug)
        except PostsModel.DoesNotExist:
            raise serializers.ValidationError("Post does not exists")
        
        attrs['post'] = post
        return attrs


class PostClapsUserSerializer(serializers.ModelSerializer):
    short_bio = serializers.CharField(source="profile.short_bio")
    avatar = serializers.ImageField(source="profile.avatar")
    is_followed = serializers.SerializerMethodField


    class Meta:
        model = User
        fields = ['short_bio','avatar','username','is_followed']
    
    @staticmethod
    def get_is_followed(obj):
        return True

class PostCommentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()


    class Meta:
        model = PostCommentModel
        fields = ['id','parent','comment','user','children']

    
    @staticmethod
    def get_children(obj):
        return obj.children.count()

class PostCommentClapsSerializer(serializers.Serializer):
    pass


        