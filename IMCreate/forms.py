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

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['title', 'description', 'tags']

class PostImageForm(forms.ModelForm):
  images = forms.ImageField(widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['comment']