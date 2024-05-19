from django.urls import path
from app.views import (
    home,
    tag_list,
    task_list,
)

urlpatterns = [
    path('', home, name='home'),
    path('get/tags/', tag_list, name='tag-list'),
    path('get/tasks/', task_list, name='task-list'),
]