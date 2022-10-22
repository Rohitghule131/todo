from django.urls import path
from todo import views

urlpatterns = [
    path("createTask/", views.CreateTaskView.as_view(), name="Create Task"),
    path("taskList/", views.ListOfTaskView.as_view(), name="Task List")
]
