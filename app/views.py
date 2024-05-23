from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import (
    Tag,
    Task,
)
from .serializers import (
    TaskSerializer,
    TaskCreateUpdateSerializer,
)

def home(request):
    return HttpResponse("Hello World")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tag_list(request):
    #tags = Tag.objects.all()
    tags_name = Tag.objects.values_list('name', flat=True)
    #print(f"\ntags_name : {tags_name}\n")
    return Response(tags_name)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_pending_list(request):
    tasks = Task.objects.filter(status='Pending')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_completed_list(request):
    tasks = Task.objects.filter(status='Completed')
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

    serializer = TaskSerializer(task)
    return Response(serializer.data)



@api_view(['POST'])
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