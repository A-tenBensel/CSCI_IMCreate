from django import forms
from .models import Post, Comment, Profile
from django.contrib.auth.models import User

class UserCreateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username', 'password']

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['about_me', 'profile_pic']
    widgets = {'profile_pic': forms.FileInput()}


class MultipleFileInput(forms.ClearableFileInput):
  allow_multiple_selected = True

class MultipleFileField(forms.FileField):
  def __init__(self, *args, **kwargs):
    kwargs.setdefault("widget",MultipleFileInput(attrs={'accept': 'image/png, image/jpeg'}))
    super().__init__(*args,**kwargs)
  def clean(self,data,initial=None):
    single_file_clean = super().clean
    if isinstance(data, (list, tuple)):
      result = [single_file_clean(d, initial) for d in data]
    else:
      result = [single_file_clean(data, initial)]
    return result

class PostImageForm(forms.Form):
  images = MultipleFileField()

class PostForm(forms.ModelForm):
  images = MultipleFileField()
  class Meta:
    model = Post
    fields = ['title', 'description', 'tags']


class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['comment']