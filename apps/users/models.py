from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from IMCreate.image_upload import pfp_path
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  display_name = models.CharField(max_length=150, blank=True)
  about_me = models.TextField(max_length = 1000, blank = True)
  profile_pic = ResizedImageField(size=[150,150], crop=['top','left'], quality=50, upload_to=pfp_path,force_format="JPEG", blank=True, null=True)

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
    Profile.objects.create(user=instance, display_name=instance.username)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()
