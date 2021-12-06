from django.urls import path
#posts
from .views import home, thread, subforum, create_post, latest_posts
urlpatterns = [
    path("", home, name="home"),
    path("subforum/<slug>/", subforum, name="subforum"),
    path("thread/<slug>/", thread, name="thread"),
    path("create_post", create_post, name="create_post"),
    path("latest_posts", latest_posts, name="latest_posts"),
]