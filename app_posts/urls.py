from django.urls import path

from app_posts.views import PostAPIView,PostDetailAPIView,PersonalPostListAPIView,PostClapsAPIView,PostCommentListAPIView

app_name = "posts"

urlpatterns = [
    path('', PostAPIView.as_view(), name='list'),
    path('me/',PersonalPostListAPIView.as_view(),name='my-posts'),
    path('<slug:slug>/', PostDetailAPIView.as_view(), name='detail'),
    path('<slug:slug>/claps/',PostClapsAPIView.as_view(),name='claps'),
    path('<slug:slug>/comments/',PostCommentListAPIView.as_view(),name='comments'),
    path('<slug:slug>/comments/claps',PostAPIView.as_view(),name='comments-claps'),
]
