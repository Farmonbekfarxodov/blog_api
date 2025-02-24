from django.forms import ValidationError
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated


from app_common.permissions import IsOwnerOrReadOnly
from app_posts.models import PostClapsModel, PostCommentModel, PostsModel
from app_posts.serializers import PostClapsUserSerializer, PostCommentModelSerializer, PostCommentSerializer, PostSerializer
from app_common.paginations import StandartResultsSetPagination

User = get_user_model()
class PostAPIView(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class  = StandartResultsSetPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        posts = PostsModel.objects.all()
        paginator = self.pagination_class()
        paginated_posts = paginator.paginate_queryset(posts, request, view=self)

        serializer = self.serializer_class(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data) 

    def get_serializer(self,*args,**kwargs):
        return self.serializer_class(*args,**kwargs)

class PostDetailAPIView(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, slug):
        post = self.get_object(slug=slug)
        self.check_object_permissions(request,post)
        serializer = self.serializer_class(post)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def put(self, request, slug):
        post = self.get_object(slug=slug)
        self.check_object_permissions(request,post)
        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug):
        post = self.get_object(slug=slug)
        self.check_object_permissions(request,post)
        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)


        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        post = self.get_object(slug=slug)
        self.check_object_permissions(request,post)
        post.delete()
        return Response( status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_object(slug):
        try:
            return PostsModel.objects.get(slug=slug)
        except PostsModel.DoesNotExist:
            raise NotFound({
                "success": False,
                "detail": "Post does not found"
            })
    
class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = PostsModel.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class PersonalPostListAPIView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandartResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PostsModel.objects.filter(author=self.request.user).order_by('-id')

class PostClapsAPIView(APIView):
    serializer_class = PostClapsUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_classes = StandartResultsSetPagination

    def get(self,request,slug):
        post = self.get_object(slug=slug)
        claps = PostClapsModel.objects.filter(post=post)
        
        claps_count = claps.count()
        users_ids = claps.values_list('user_id',flat=True).distinct()
        users_count = users_ids.count()

        users_objects = User.objects.filter(id__in=users_ids).order_by('-id')

        paginator = self.pagination_class()
        paginated_users = paginator.paginate_query_set(users_objects,request)
        serializer = self.serializer_class(paginated_users,many=True)


        return Response(data={
            "claps_count":claps_count,
            "users_count":users_count,
            "users":serializer.data
        },status=status.HTTP_200_OK)
       
    def post(self,request,slug):
        post = self.get_object(slug=slug)
        user = request.user

        PostClapsModel.objects.create(user=user,post=post)
        claps_count = self.get_claps_count(post=post)
        return Response(data={"claps_count":claps_count},
                        status = status.HTTP_201_CREATED)
    
    def get_claps_count(self,post):
        return PostClapsModel.objects.filter(user=self.request.user,post=post).count()
    
    @staticmethod
    def get_object(slug):
        try:
            return PostsModel.objects.get(slug=slug)
        except PostsModel.DoesNotExist:
            raise ValidationError("Post does not exists")
    
    def get_serializer(self,*args,**kwargs):
        return self.serializer_class(*args,**kwargs)

class PostCommentListAPIView(ListAPIView):
    
    pagination_class = StandartResultsSetPagination
    permission_classes = [IsAuthenticated]
    serializer_class = PostCommentSerializer

    def get_queryset(self):
        return PostCommentModel.objects.order_by('-id')

class PostCommentCreateAPIView(CreateAPIView):
    queryset = PostCommentModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostCommentModelSerializer