from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView, DetailView

from IMCreate.forms.forms import ProfileForm
from IMCreate.forms.render import RenderForm
from IMCreate.render import RenderUserCreationForm, RenderAuthenticationForm
from .models import Profile

class ProfileEditView(UserPassesTestMixin, UpdateView):
  model = Profile
  form_class = ProfileForm
  template_name = 'profile_edit.html'
  # slug_url_kwarg = "user_slug"
  login_url = "login_user"
  redirect_field_name = None

  def get_object(self):
    return self.request.user.profile

  def test_func(self):
    if self.request.user.is_authenticated:
      return self.request.user.profile.slug == self.get_object().slug
    else:
      return False

class UserCreateView(UserPassesTestMixin, CreateView):
  model = User
  form_class = UserCreationForm
  template_name = "sign_up.html"
  success_url = reverse_lazy("user_account")
  def form_valid(self, form):
    response = super().form_valid(form)
    login(self.request, self.object)
    return response
  
  def test_func(self):
    return not self.request.user.is_authenticated

  def dispatch(self, request, *args, **kwargs):
    user_test_result = self.get_test_func()()
    if not user_test_result:
      return redirect('user_account')
    return super().dispatch(request, *args, **kwargs)

class UserAuthenticationView(UserPassesTestMixin, FormView):
  form_class = AuthenticationForm
  template_name = "login.html"
  success_url = reverse_lazy("user_account")

  def form_valid(self, form):
    user = authenticate(self.request, **form.cleaned_data)
    if user is not None:
      login(self.request, user)
    return super().form_valid(form)
  
  def test_func(self):
    return not self.request.user.is_authenticated
  
  def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return redirect("update_profile")
        return super().dispatch(request, *args, **kwargs)

class ProfileView(DetailView):
  model = Profile
  slug_url_kwarg = "profile_slug"
  template_name = "profile.html"

def sign_up(request):
  if request.user.is_authenticated:
    return redirect("update_profile")
  return RenderUserCreationForm(request).render
  
def login_user(request):
  if request.user.is_authenticated:
    return redirect("update_profile")
  return RenderAuthenticationForm(request).render

def update_profile(request):
  if not request.user.is_authenticated:
    return redirect("login_user")
  print(request.user.profile.profile_pic)
  return RenderForm(request, ProfileForm, view='account.html', form_kwargs={"instance": request.user.profile}).render