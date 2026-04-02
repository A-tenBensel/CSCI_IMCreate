from django.contrib.auth import login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Post

def front_page(request):
  tags = request.GET.get("tags","").strip()
  if request.method == "POST":
    tags = request.POST.get("tags","").strip()
    tagsList = tags.split(',')
    for i in range(len(tagsList)):
      tagsList[i] = tagsList[i].strip()
  if tagsList:
    posts = Post.objects.filter(tags__name__in=tagsList).order_by("upload_date")
  else:
    posts = Post.objects.all().order_by("upload_date")
  return render(request,'index.html',{'posts':posts, 'tags':tags})
