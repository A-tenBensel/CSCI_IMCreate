from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from IMCreate.render import RenderPostForm
from apps.posts.models import Post
from apps.social.models import Like
from django.shortcuts import render, get_object_or_404

def make_post(request):
  return RenderPostForm(request,view='make_post.html').render


def view_post(request, post_id):
  post = get_object_or_404(Post, id=post_id)

  liked_posts = set()

  if request.user.is_authenticated:
    liked_posts = set(
      Like.objects.filter(user=request.user).values_list("post_id", flat=True)
    )

  return render(request, 'components/post.html', {
    'post': post,
    'liked_posts': liked_posts
  })

@login_required
def like_post(request, post_id):
  post = Post.objects.get(id=post_id)

  like, created = Like.objects.get_or_create(
    user=request.user,
    post=post
  )

  if created:
    post.like_count += 1
    post.save()

  return JsonResponse({'count': post.like_count, 'liked': True})


@login_required
def unlike_post(request, post_id):
  post = Post.objects.get(id=post_id)

  deleted, _ = Like.objects.filter(
    user=request.user,
    post=post
  ).delete()

  if deleted:
    post.like_count -= 1
    post.save()

  return JsonResponse({'count': post.like_count, 'liked': False})