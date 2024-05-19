from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Tag,
    Task,
)
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
)

def home(request):
    return HttpResponse("Hello World")


@api_view(['GET'])
def tag_list(request):
    #tags = Tag.objects.all()
    tags_name = Tag.objects.values_list('name', flat=True)
    #print(f"\ntags_name : {tags_name}\n")
    return Response(tags_name)


@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_task(request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)