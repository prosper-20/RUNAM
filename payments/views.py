from django.shortcuts import render
from rest_framework.views import APIView
from tasks.models import Task
from tasks.serializers import TaskSerializer
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
    
