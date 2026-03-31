from django.contrib.auth import login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from apps.posts.models import Post

def front_page(request):
  return render(request, "index.html", {"posts": Post.objects.all})
