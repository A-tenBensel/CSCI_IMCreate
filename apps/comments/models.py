from django.db import models
from django.contrib.auth.models import User
from apps.posts.models import Post

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
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  last_edit_date = models.DateTimeField(auto_now = True)
  comment = models.TextField(max_length = 1000)
  post = models.ForeignKey(Post, related_name="replies", on_delete=models.CASCADE)
  parent = models.ForeignKey("self", null=True,blank=True,on_delete=models.CASCADE,related_name="replies")
