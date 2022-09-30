from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("signup/", views.SignUpUserView.as_view(), name="Sign Up"),
    path("all-users/", views.GetAllUsersView.as_view(), name="All Users"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signin/", views.SignInUserView.as_view(), name="Sign In"),
    path("signout/", views.SignOutUserView.as_view(), name="Sign Out"),
    path("changepassword/", views.ChangeUserPasswordView.as_view(), name="Change Password"),
]
