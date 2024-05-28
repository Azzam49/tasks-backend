from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, F, Case, When, IntegerField
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import (
    Tag,
    Task,
)
from .serializers import (
    TagSerializer,
    TaskSerializer,
    TaskCreateUpdateSerializer,
    SingleTaskSerializer,
)

def home(request):
    return HttpResponse("Hello World")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tag_list(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    #print(f"\ntags_name : {tags_name}\n")
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request):
    if request.user.is_staff:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(owner=request.user)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_pending_list(request):
    if request.user.is_staff:
        tasks = Task.objects.filter(status='Pending')
    else:
        tasks = Task.objects.filter(owner=request.user, status='Pending')

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_completed_list(request):
    if request.user.is_staff:
        tasks = Task.objects.filter(status='Completed')
    else:
        tasks = Task.objects.filter(owner=request.user, status='Completed')

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

# @api_view(['POST'])
# def create_task(request):
#     serializer = TaskCreateSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    try:
        serializer = TaskCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Raise exception on validation failure
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as exc:
        print(f"\nexc.detail: {exc.detail}\n")
        error_message = exc.detail#.get('non_field_errors', [])
        # if error_message:
        #     error_message = error_message[0]
        # else:
        #     error_message = exc.detail
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskCreateUpdateSerializer(task, data=request.data)
    try:
        serializer.is_valid(raise_exception=True)  # Raise exception on validation failure
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValidationError as exc:
        print(f"\nexc.detail: {exc.detail}\n")
        error_message = exc.detail
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    task.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task_as_completed(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if task.status == "Completed":
        return Response({"detail": "This task status is already set as Completed."}, status=status.HTTP_404_NOT_FOUND)

    # change task status
    task.status = "Completed"
    task.completed_at = timezone.now()
    task.save()

    # without return {} it returns nothing and by nothing the react was facing json parse error
    return Response({}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_by_id(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = SingleTaskSerializer(task)
    return Response(serializer.data)



@api_view(['POST'])
@authentication_classes([])
def register_user(request):
    # Extract the necessary fields from the request data
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    # Validate input
    if not username or not password or not email:
        return Response({'error': 'Username, password, and email are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the username already exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = User.objects.create_user(username=username, password=password, email=email)

    return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def charts_data(request):

    user = request.user
    if user.is_staff:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(owner=user)

    # Get the total number of tasks, and count by status
    total_tasks_count = tasks.count() #Task.objects.count()
    pending_tasks_count = tasks.filter(status='Pending').count() #Task.objects.filter(status='Pending').count()
    completed_tasks_count = tasks.filter(status='Completed').count() #Task.objects.filter(status='Completed').count()

    # Get the count of tasks for each tag
    # tags_data = Tag.objects.annotate(task_count=Count('task')).values('name', 'task_count')
    if user.is_staff:
        tags_data = Tag.objects.annotate(task_count=Count('task')).values('name', 'task_count')
    else:
        tags_data = Tag.objects.annotate(
            task_count=Count(
                Case(
                    When(task__owner=user, then=1),
                    output_field=IntegerField()
                )
            )
        ).values('name', 'task_count')
    tag_labels = [tag['name'] for tag in tags_data]
    tag_values = [tag['task_count'] for tag in tags_data]

    # Get the count of completed tasks per day for the last 10 days
    today = timezone.now().date()
    ten_days_ago = today - timedelta(days=9)  # adjust to get full range of 10 days
    #
    # completed_tasks_data = Task.objects.filter(
    completed_tasks_data = tasks.filter(
        completed_at__date__gte=ten_days_ago,
        status='Completed'
    ).values(
        day=F('completed_at__date')
    ).annotate(
        count=Count('id')
    ).order_by('day')
    #
    # print(f"\n\nORM - completed_tasks_data : {completed_tasks_data}\n\n")
    # print result : #ORM - completed_tasks_data : <QuerySet [{'day': datetime.date(2024, 5, 26), 'count': 1}]>
    # Create a dictionary to map each date to its task count
    task_date_count = {task['day']: task['count'] for task in completed_tasks_data}
    # Generate the full list of dates in the last 10 days
    completed_task_labels = [(today - timedelta(days=i)).strftime('%b %d') for i in range(9, -1, -1)]
    # `i` starts at 9, stops at `-1`, each iterate it get decreased by `-1`
    completed_task_values = [
        task_date_count.get(today - timedelta(days=i), 0)  # Get the count if exists, else 0
        for i in range(9, -1, -1)
    ]
    #
    # print(f"\n\ncompleted_task_labels : {completed_task_labels}, len: {len(completed_task_labels)}")
    # print(f"completed_task_values : {completed_task_values}")
    # print(f"task_date_count : {task_date_count}")
    # print(f"fixed - task_values : {task_values}\n\n")

    data = {
        'total_tasks_count': total_tasks_count,
        'pending_tasks_count': pending_tasks_count,
        'completed_tasks_count': completed_tasks_count,

        'tag_labels': tag_labels,
        'tag_values': tag_values,

        'completed_task_labels': completed_task_labels,
        'completed_task_values': completed_task_values
    }
    return Response(data)