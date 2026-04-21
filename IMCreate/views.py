from django.contrib.auth import login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from apps.posts.models import Post
from apps.social.models import Follower, Blocked

def front_page(request):
  tags = request.GET.get("tags","").strip()

  if tags:
    tagsList = [t.strip() for t in tags.split(',') if t.strip()]
    posts = Post.objects.filter(tags__name__in=tagsList).distinct()

  else:
    posts = Post.objects.all()

  posts = posts.order_by("upload_date")
  if request.user.is_authenticated:
    blocked_accounts = request.user.blocks.all()
    for blocked in blocked_accounts:
      posts = posts.exclude(user=blocked.blocked_user)
    following = request.user.following.all()
    is_following = [following.filter(following=post.user).exists() for post in posts]
  else:
    is_following = [False for _ in posts]
  return render(request,'index.html',{'posts':zip(posts, is_following), "tags_query": tags})
