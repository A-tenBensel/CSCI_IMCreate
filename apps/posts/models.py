from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django_resized import ResizedImageField
from IMCreate.image_upload import post_image_path

class Post(models.Model):
  """

  TODO: All media, just images, file compression.

  The data for a post.

  Attributes:
  user: User that posted post.
  upload_date: Post upload date.
  edit_date: Last edit date.
  title: User provided title.
  description: user provided description.
  tags: User provided tags.
  """
  user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
  upload_date = models.DateTimeField(auto_now_add = True)
  edit_date = models.DateTimeField(auto_now = True)
  title = models.CharField(max_length = 255)
  description = models.TextField(max_length = 1000)
  tags = TaggableManager()

class Post_Image(models.Model):
  post = models.ForeignKey(Post, related_name="images", on_delete=models.CASCADE)
  image = ResizedImageField(size=[480,None],quality=50,upload_to=post_image_path, force_format="JPEG")
