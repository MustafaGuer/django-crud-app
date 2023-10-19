from typing import Any
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import TodoList, TodoItem

# Create your views here.

class TodoListsView(ListView):
    model = TodoList
    template_name = "todo_app/index.html"


class TodoItemView(ListView):
    model=TodoItem
    template_name="todo_app/todo_list.html"
    
    def get_queryset(self):
        return TodoItem.objects.filter(todo_list_id=self.kwargs["list_id"])
    
    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = TodoList.objects.get(id=self.kwargs["list_id"])
        return context
    

class ListCreateView(CreateView):
    model = TodoList
    fields = ["title"]
    
    def get_context_data(self):
        context = super(ListCreateView, self).get_context_data()
        context["title"] = "Neue Liste hinzufügen"
        return context
    

class ItemCreate(CreateView):
    model = TodoItem
    fields = ["todo_list", "title", "description", "due_date"]
    
    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = TodoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data
    
    
    def get_context_data(self):
        context = super(ItemCreate,self).get_context_data()
        todo_list = TodoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Neues Todo hinzufügen"
        return context
    
    def get_succcess_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ItemUpdate(UpdateView):
    model = TodoItem
    fields = ["todo_list", "title", "description", "due_date"]
    
    def get_context_data(self):
        context = super(ItemUpdate,self).get_context_data()

        context["todo_list"] = self.object.todo_list
        context["title"] = "Todo bearbeiten"
        return context
    
    def get_succcess_url(self):
        return reverse("list", args=[self.object.todo_list_id])
    

class ListDelete(DeleteView):
    model = TodoList
    
    success_url = reverse_lazy("index")


class ItemDelete(DeleteView):
    model = TodoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context