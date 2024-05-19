from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    Tag,
    Task,
)
from .serializers import (
    TaskSerializer
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