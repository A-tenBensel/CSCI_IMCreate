from django.urls import path
from .views import *

urlpatterns = [
  path('comment/<int:post_id>', comment, name='comment'),
]