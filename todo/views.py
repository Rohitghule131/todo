from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from utils.renderers import ResponseInfo
from user.permissions import TokenAuthentication
from todo.serializer import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from todo.models import ToDoTaskModel


class CreateTaskView(CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [TokenAuthentication, IsAuthenticated]

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateTaskView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.response_format["message"] = "Task Created Successfully"
        self.response_format["error"] = None
        self.response_format["status_code"] = status.HTTP_201_CREATED
        self.response_format["data"] = serializer.data

        return Response(self.response_format)


class ListOfTaskView(RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [TokenAuthentication, IsAuthenticated]
    lookup_field = ["pk"]

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ListOfTaskView, self).__init__(**kwargs)

    def get_queryset(self):

        queryset = ToDoTaskModel.objects.filter(user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        self.response_format["message"] = "Your Task List Fetch Successfully"
        self.response_format["error"] = None
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["data"] = serializer.data

        return Response(self.response_format)

