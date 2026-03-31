from django.urls import path
from apps.posts import views as post_views
from apps.users import views as user_views
from apps.comments import views as comment_views
from apps.social import views as social_views
from IMCreate import views

urlpatterns = [
  path("",                    views.front_page,       name="front_page"),
  path("account",             user_views.update_profile,   name="update_profile"),
  path("make_post",           post_views.make_post,        name="make_post"),
  path("post/<int:post_id>/", post_views.view_post,        name="view_post"),
]