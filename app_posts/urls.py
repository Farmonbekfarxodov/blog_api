from django.urls import path

from app_posts.views import (PostAPIView,PostDetailAPIView,PersonalPostListAPIView,
                             PostClapsAPIView,PostCommentListCreateAPIView)

app_name = "posts"

urlpatterns = [
    path('', PostAPIView.as_view(), name='list'),
    path('me/',PersonalPostListAPIView.as_view(),name='my-posts'),
    path('<slug:slug>/', PostDetailAPIView.as_view(), name='detail'),
    path('<slug:slug>/claps/',PostClapsAPIView.as_view(),name='claps'),
    
     path('<slug:slug>/comments/',PostCommentListCreateAPIView.as_view(),name='comments'),
    # path('comments/<int:pk>/',CommentChildrenListAPIView.as_view(),name='comments_children'),
    # path('comments/<int:pk>/claps/',CommentClapsListCreateAPIView.as_view(),name='comments_claps'),
]
