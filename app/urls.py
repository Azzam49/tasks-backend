from django.urls import path
from app.views import (
    home,
    tag_list,
)

urlpatterns = [
    path('', home, name='home'),
    path('tags/', tag_list, name='tag-list'),
]