from django.contrib.auth import login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from apps.posts.models import Post

def front_page(request):
  tags = request.GET.get("tags","").strip()

  if tags:
    tagsList = [t.strip() for t in tags.split(',') if t.strip()]
    posts = Post.objects.filter(tags__name__in=tagsList).distinct()

  else:
    posts = Post.objects.all()
  
  posts = posts.order_by("upload_date")
  
  return render(request,'index.html',{'posts':posts, "tags_query": tags})
