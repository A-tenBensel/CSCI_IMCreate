from django.shortcuts import render
from IMCreate.render import RenderPostForm
from apps.posts.models import Post

def make_post(request):
  return RenderPostForm(request,view='make_post.html').render

def view_post(request, post_id):
  post = Post.objects.get(id=post_id)
  return render(request, 'components/post.html',{'post': post})
