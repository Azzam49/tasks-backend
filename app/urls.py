from django.urls import path
from app.views import (
    home,
    tag_list,
    task_list,
    create_task,
    update_task,
)

urlpatterns = [
    path('', home, name='home'),
    path('get/tags/', tag_list, name='tag-list'),
    path('get/tasks/', task_list, name='task-list'),
    path('post/task/', create_task, name='create-task'),
    path('put/task/<id>/', update_task, name='update_task'),
]