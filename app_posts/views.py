from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from app_posts.models import PostsModel
from app_posts.serializers import PostsSerializer


class PostAPIView(APIView):
    serializer_class = PostsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        posts = PostsModel.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostDetailAPIView(APIView):
    serializer_class = PostsSerializer

    def get(self, request, slug):
        post = self.get_object(slug=slug)
        serializer = self.serializer_class(post)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, slug):
        post = self.get_object(slug=slug)
        serializer = PostsSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data={
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_202_ACCEPTED)

        return Response(data={
            "success": False,
            "detail": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug):
        post = self.get_object(slug=slug)
        serializer = PostsSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data={
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_202_ACCEPTED)


        return Response(data={
            "success": False,
            "detail": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        post = self.get_object(slug=slug)
        post.delete()
        return Response(data={
            "success": True,
            "detail": "Post is deleted"
        }, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_object(slug):
        try:
            return PostsModel.objects.get(slug=slug)
        except PostsModel.DoesNotExist:
            raise NotFound({
                "success": False,
                "detail": "Post does not found"
            })
