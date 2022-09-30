from rest_framework.permissions import BasePermission
from user.models import BlackListedToken


class TokenAuthentication(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header:
            key, token = auth_header.split(" ")
            if key == "Bearer":
                try:
                    BlackListedToken.objects.get(token=token)
                    is_auth_user = False
                except BlackListedToken.DoesNotExist:
                    is_auth_user = True
            else:
                is_auth_user = False
        else:
            is_auth_user = False
        return is_auth_user
