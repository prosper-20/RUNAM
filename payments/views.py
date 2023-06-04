from django.shortcuts import render
from rest_framework.views import APIView
from tasks.models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ViewAllTask(APIView):
    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CreateNewTask(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        new = Task(sender=request.user)
        serializer = TaskSerializer(new, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

