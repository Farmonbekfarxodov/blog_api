from django.urls import path

from app_posts.views import posts_view,post_detail_view

app_name = "posts"

urlpatterns = [
    path('<slug:slug>/', post_detail_view, name='detail'),
    path('', posts_view, name='list'),
]
