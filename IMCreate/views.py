from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import ProfileForm, PostForm, PostImageForm
from .models import User, Post, Comment, Like, Follower, Blocked, Post_Image


def basic_save(request, obj):
  obj.save()
  return None

def make_forms(request, *forms, **attrs):
  ret_forms = []
  if request.method == "POST":
    for index in range(len(forms)):
      temp = forms[index](request.POST, request.FILES, **attrs.get(f"args{index}",dict()))
      ret_forms.append(temp)
      if temp.is_valid():
        temp_ret = attrs.get(f"save{index}",basic_save)(request, temp)
        if temp_ret is not None:
          return temp_ret
  else:
    ret_forms = [forms[index](**attrs.get(f"args{index}",dict())) for index in range(len(forms))]
  return ret_forms

def make_form(request, form, save= basic_save, args=dict()):
  return make_forms(request, form, args0=args, save0=save)

def front_page(request):
  return

def sign_up(request):
  if request.user.is_authenticated:
    return redirect(reverse("update_profile"))
  form = make_form(request, UserCreationForm)[0]
  if request.method == "POST" and form.is_valid():
    user = form.save()
    login(request, user)
    return redirect(reverse("update_profile"))
  return render(request, "sign_up.html", {"form": form})
  
def update_profile(request):
  profile_form = make_form(request, ProfileForm, {"instance": request.user.profile})[0]
  return render(request, 'account.html', {'form': profile_form, "pfp": request.user.profile.profile_pic})

def make_post(request):
  def make_images(request, obj):
    post = obj.save(commit = False)
    post.user = request.user
    post.save()
    images = obj.cleaned_data['images']
    for image in images:
      Post_Image.objects.create(post=post, image=image)
    return redirect('view_post',post_id=post.id)
    
  forms = make_form(request, PostForm, save = make_images)
  if type(forms) != type([]):
    return forms
  return render(request, 'make_post.html', {'forms': forms})

def view_post(request, post_id):
  post = Post.objects.get(id=post_id)
  return render(request, 'components/post.html',{'post': post})

"""

def front_page(request):
  return create_account(request)

def create_account(request):
  success = False
  account = None
  if request.method == "POST":
    form = UserForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      success = True
      return redirect('front_page')
  else:
    form = UserForm()
  return render(request, "account.html", {"form": form, "success": success},)

def follow_user(request, user_id):
  print(f"[DBG] follow_user {user_id} <<<")
  current_user = request.User
  if request.method == "POST" and current_user.is_authenticated:
    Follower.objects.create(following=User.objects.get(id=user_id), follower=current_user)

  return redirect(request.path)

def block_user(request, user_id):
  print(f"[DBG] block_user {user_id} <<<")
  current_user = request.User
  if request.method == "POST" and current_user.is_authenticated:
    Blocked.objects.create(blocked_user=User.objects.get(id=user_id), blocker=current_user)

  return redirect(request.path)

def get_post(request, post_slug):
  post = get_object_or_404(Post, slug=post_slug)
  return render(request, "components/post.html",post = post)

def like_post(request, post_id):
  post = get_object_or_404(Post, id=post_id)
  user = request.User
  if user.is_authenticated and post:
    Like.objects.create(user=user, post=post)
  return redirect(request.path)

def get_user(request, user_id):
  user = User.objects.get(id=user_id)
  return render(request, "user_page.html", user=user)

"""