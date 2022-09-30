from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from user import signals
from user.models import CustomUser
from utils.renderers import ResponseInfo
from user.serializer import (
    SignUpSerializer,
    GetUsers,
    SignUserSerializer,
    ChangeUserPasswordSerializer,
    SignOutUserSerializer
)
from user.permissions import TokenAuthentication


class SignUpUserView(CreateAPIView):
    serializer_class = SignUpSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(SignUpUserView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.response_format["data"] = serializer.data
        self.response_format["status_code"] = status.HTTP_201_CREATED
        self.response_format["error"] = None
        self.response_format["message"] = ["Sign up successfully :)"]
        return Response(self.response_format)


class GetAllUsersView(ListAPIView):
    serializer_class = GetUsers
    queryset = CustomUser
    lookup_field = ['pk']
    permission_classes = [IsAuthenticated, TokenAuthentication]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(CustomUser.objects.all(), many=True)
        return Response(serializer.data)


class SignInUserView(CreateAPIView):
    serializer_class = SignUserSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(SignInUserView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        signals.Login_User.send(request.data["email"])
        self.response_format["data"] = serializer.data
        self.response_format["status_code"] = status.HTTP_201_CREATED
        self.response_format["error"] = None
        self.response_format["message"] = ["Sign In Successfully :)"]
        return Response(self.response_format)


class SignOutUserView(CreateAPIView):
    serializer_class = SignOutUserSerializer
    permission_classes = [IsAuthenticated, TokenAuthentication]
    authentication_classes = [JWTAuthentication]

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(SignOutUserView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        auth_user = request.META.get('HTTP_AUTHORIZATION')
        key, token = auth_user.split(" ")
        request.data['token'] = token
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        signals.Logout_User.send(request.user.email)
        self.response_format["data"] = []
        self.response_format["status_code"] = status.HTTP_201_CREATED
        self.response_format["error"] = None
        self.response_format["message"] = ["Sign Out Successfully :)"]
        return Response(self.response_format)


class ChangeUserPasswordView(CreateAPIView):
    serializer_class = ChangeUserPasswordSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, TokenAuthentication]

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ChangeUserPasswordView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.response_format["data"] = []
        self.response_format["status_code"] = status.HTTP_201_CREATED
        self.response_format["error"] = None
        self.response_format["message"] = ["Change Password Successfully :)"]
        return Response(self.response_format)
