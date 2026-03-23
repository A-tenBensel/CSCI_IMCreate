from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField
from taggit.managers import TaggableManager
from PIL import Image
import uuid
from django.conf import settings

def img_name(instance, filename):
  print("IMAGE")
  try:
    directory = instance.user.id
  except AttributeError:
    directory = instance.post.user.id
  except Exception as e:
    print(f"ERRORRRR {e}")
    directory = "ERROR"
  return f"{directory}/{uuid.uuid4().hex}.jpeg"

# def img_file_at(directory):
#   def img_name(instance, filename):
#     return f"{directory}/{uuid.uuid4().hex}.jpeg"
#   return img_name

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  about_me = models.TextField(max_length = 1000, blank = True)
  profile_pic = ResizedImageField(size=[150,150], crop=['top','left'], quality=50, upload_to=img_name,force_format="JPEG", blank=True, null=True)

  def save(self, *args, **kwargs):
    try:
      old = Profile.objects.get(pk=self.pk)
    except Profile.DoesNotExist:
      old = None
    super().save(*args, **kwargs)
    if old and old.profile_pic and old.profile_pic != self.profile_pic:
      old.profile_pic.delete(save=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()

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
  user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE)
  upload_date = models.DateTimeField(auto_now_add = True)
  edit_date = models.DateTimeField(auto_now = True)
  title = models.CharField(max_length = 255)
  description = models.TextField(max_length = 1000)
  tags = TaggableManager()
  # media = models.FileField(upload_to = posts)

class Post_Image(models.Model):
  post = models.ForeignKey(Post, related_name="images", on_delete=models.CASCADE)
  image = ResizedImageField(size=[480,None],quality=50,upload_to=img_name, force_format="JPEG")

class Comment(models.Model):
  """

  The data for comments.

  Attributes:
  user: The User that posted the comment.
  last_edit_date: Last edit date of the comment.
  comment: The text of the comment.
  post: The post the comment is linked to.
  parent: If part of a comment chain on a post, the parent comment, else None.
  """
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  last_edit_date = models.DateTimeField(auto_now = True)
  comment = models.TextField(max_length = 1000)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  parent = models.ForeignKey("self", null=True,blank=True,on_delete=models.CASCADE,related_name="replies")

class Like(models.Model):
  """

  The data for likes.

  Attributes:
  user: User that gave the like.
  post: Post that the user liked.
  """
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  class Meta:
    constraints = [models.UniqueConstraint(fields=['user', "post"], name = 'unique_like')]

class Follower(models.Model):
    """

    The data for following a specific user.

    Attributes:
    following: Account that is being followed.
    follower: User that is following.
    notifications: If the follower gets notifs when following posts.
    """
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='following')
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='follower')
    notifications = models.BooleanField(default = True)
    class Meta:
      # unique_together = ("follower", "following")
      constraints = [models.UniqueConstraint(fields=['follower', "following"], name = 'unique_follow')]

class Blocked(models.Model):
    """
    Blocked Accounts.

    Attributes:
    blocked_user: The account that is blocked.
    blocker: The account that did the blocking.
    """
    blocker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='blocker')
    blocked_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocked')
    class Meta:
      # unique_together = ("blocker", "blocked_user") getting deprecated
      constraints = [models.UniqueConstraint(fields=['blocker', "blocked_user"], name = 'unique_block')]