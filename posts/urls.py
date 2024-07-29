from django.urls import path 
from . import views


urlpatterns = [
    path('homepage', views.homepage),
    path('posts', views.PostListCreateView.as_view()),
    path('posts/<int:post_id>', views.PostRetriveUpdateDeleteView.as_view()),
    path("current_user/", views.get_posts_for_current_user),
    path("list_post/", views.list_posts_for_author),

]