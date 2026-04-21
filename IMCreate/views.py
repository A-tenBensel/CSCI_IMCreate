from django.contrib.auth import login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from apps.posts.models import Post
from apps.social.models import Like

def front_page(request):
  tags = request.GET.get("tags", "").strip()

  if tags:
    tagsList = [t.strip() for t in tags.split(',') if t.strip()]
    posts = Post.objects.filter(tags__name__in=tagsList).distinct()
  else:
    posts = Post.objects.all()

  posts = posts.order_by("upload_date")

  liked_posts = set()

  if request.user.is_authenticated:
    liked_posts = set(
      Like.objects.filter(user=request.user).values_list("post_id", flat=True)
    )

  return render(request, 'index.html', {
    'posts': posts,
    'tags_query': tags,
    'liked_posts': liked_posts
  })
