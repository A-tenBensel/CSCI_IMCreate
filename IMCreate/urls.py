from django.urls import path

from .views import front_page, sign_up, update_profile, make_post, view_post

urlpatterns = [
  path("", sign_up,name="front_page"),
  path("account",update_profile, name="update_profile"),
  path("make_post",make_post,name="make_post"),
  path("post/<int:post_id>/",view_post,name="view_post"),
  # path("post/<str:post_slug>",get_post, name="get_post"),
  # path("follow/<int:user_id>", follow_user, name="follow_user"),
  # path("block/<int:user_id>", block_user, name="block_user"),
  # path("like/<int:post_id>", like_post, name="like_post"),
  # path("user/<int:user_id>", get_user, name="get_user"),
]