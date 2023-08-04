from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden,HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from tasks.models import Task

@login_required
def task_chat_room(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        # user is not a student of the course or course does not exist
        return HttpResponseNotFound()
    return render(request, 'chat/room.html', {'task': task})

# Create your views here.
