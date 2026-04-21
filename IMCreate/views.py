from django.contrib.auth import login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from apps.posts.models import Post
from apps.social.models import Like

def front_page(request):
  tags = request.GET.get("tags","").strip()
  sortBy = request.GET.get("sortBy")
  if tags:
    tagsList = [t.strip() for t in tags.split(',') if t.strip()]
    posts = Post.objects.filter(tags__name__in=tagsList).distinct()
  else:
    posts = Post.objects.all()
  
  if sortBy == "Recent":
    posts = posts.order_by("upload_date").reverse()
  elif sortBy == "Likes":
    posts = posts.order_by("title").reverse()
  else:
    posts = posts.order_by("upload_date").reverse()

  paginator = Paginator(posts, 2)
  pageNumber = request.GET.get("page",1)
  try:
    pageObj = paginator.get_page(pageNumber)
  except PageNotAnInteger:
    pageObj = paginator.get_page(1)
  except EmptyPage:
    pageObj = paginator.get_page(paginator.num_pages)
  
  return render(request,'index.html',{'posts':pageObj, "tags_query": tags})
