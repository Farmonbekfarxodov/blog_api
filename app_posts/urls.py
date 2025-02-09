from django.urls import path

from app_posts.views import posts_view

app_name = "posts"

urlpatterns = [
    path('',posts_view,name='list')
]
