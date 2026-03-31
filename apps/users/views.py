from django.shortcuts import render, redirect
from IMCreate.render import RenderUserCreationForm, RenderAuthenticationForm
from IMCreate.forms.forms import ProfileForm
from IMCreate.forms.render import RenderForm

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
    return login_user(request)
  print(request.user.profile.profile_pic)
  return RenderForm(request, ProfileForm, view='account.html', form_kwargs={"instance": request.user.profile}).render

