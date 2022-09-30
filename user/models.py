from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from user.manager import CustomManager


class CustomUser(AbstractBaseUser):
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    date_of_joined = models.DateField(verbose_name="Date of joined", auto_now=False, auto_now_add=False)
    login_date = models.DateField(verbose_name="Login Date", auto_now=False, auto_now_add=False)
    logout_date = models.DateField(verbose_name="Logout Date", auto_now=False, auto_now_add=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomManager()

    def __str__(self):
        return self.email


class BlackListedToken(models.Model):
    created_at = models.DateField(verbose_name="Created At", auto_created=True)
    token = models.CharField(verbose_name="Black Listed Token", max_length=600, null=False, blank=False)

    def __str__(self):
        return self.token
