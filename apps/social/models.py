from django.db import models
from django.contrib.auth.models import User
from apps.posts.models import Post

class Like(models.Model):
  """

  The data for likes.

  Attributes:
  user: User that gave the like.
  post: Post that the user liked.
  """
  user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
  post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
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
    following = models.ForeignKey(User, on_delete = models.CASCADE, related_name='following')
    follower = models.ForeignKey(User, on_delete = models.CASCADE, related_name='follower')
    notifications = models.BooleanField(default = True)
    class Meta:
      constraints = [models.UniqueConstraint(fields=['follower', "following"], name = 'unique_follow')]

class Blocked(models.Model):
    """
    Blocked Accounts.

    Attributes:
    blocked_user: The account that is blocked.
    blocker: The account that did the blocking.
    """
    blocker = models.ForeignKey(User, on_delete = models.CASCADE, related_name='blocker')
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked')
    class Meta:
      constraints = [models.UniqueConstraint(fields=['blocker', "blocked_user"], name = 'unique_block')]