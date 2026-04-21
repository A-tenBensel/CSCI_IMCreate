from django.shortcuts import render, redirect
from django.urls import reverse
from IMCreate.render import RenderPostForm
from apps.posts.models import Post
from apps.social.models import Follower
from IMCreate.forms.forms import CommentForm

def make_post(request):
  return RenderPostForm(request,view='make_post.html').render

def view_post(request, post_id):
  post = Post.objects.get(id=post_id)
  if request.user.is_authenticated:
    is_following = request.user.following.filter(following=post.user).exists()
  else:
    is_following = False
  return render(request, 'components/post.html',{'post': post, 'is_following': is_following})

def comment(request, post_id):
  post = Post.objects.get(id=post_id)
  if not request.user.is_authenticated:
    return redirect("view_post", post_id = post.id)
  if request.method == "POST":
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
      comment = comment_form.save(commit=False)
      comment.user = request.user
      comment.post = post
      comment.save()
  else:
    comment_form = CommentForm()
  return render(request, 'components/post.html', {'post': post, "comment_form": comment_form})