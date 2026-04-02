from django.urls import path
from .views import *

urlpatterns = [
  path("sign_up", UserCreateView.as_view(), name="sign_up"),
  path("login", UserAuthenticationView.as_view(), name="login_user"),
  path("account/", ProfileEditView.as_view(), name="user_account"),
  path("<slug:profile_slug>", ProfileView.as_view(), name="view_profile"),
]