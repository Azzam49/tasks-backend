from django.urls import path
from app.views import (
    home,
    tag_list,
    task_list,
    create_task,
    update_task,
    delete_task,
    update_task_as_completed,
    get_task_by_id,
)

urlpatterns = [
    path('', home, name='home'),
    path('get/tags/', tag_list, name='tag-list'),
    path('get/tasks/', task_list, name='task-list'),
    path('post/task/', create_task, name='create-task'),
    path('put/task/<id>/', update_task, name='update_task'),
    path('delete/task/<id>/', delete_task, name='delete_task'),
    path('put/task-to-completed/<id>/', update_task_as_completed, name='update_task_as_completed'),
    path('get/task/<id>/', get_task_by_id, name='get_task_by_id'),
]