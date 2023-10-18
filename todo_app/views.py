from django.shortcuts import render

from django.views.generic import ListView
from .models import TodoList

# Create your views here.

class TodoListsView(ListView):
    model = TodoList
    template_name = "todo_app/index.html"
