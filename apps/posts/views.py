from django.shortcuts import render
from IMCreate.render import RenderPostForm
from apps.posts.models import Post
from apps.social.models import Follower

def make_post(request):
  return RenderPostForm(request,view='make_post.html').render

def view_post(request, post_id):
  post = Post.objects.get(id=post_id)
  if request.user.is_authenticated:
    is_following = request.user.following.filter(following=post.user).exists()
  else:
    is_following = False
  return render(request, 'components/post.html',{'post': post, 'is_following': is_following})
