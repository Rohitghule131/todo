from django.contrib.auth.base_user import BaseUserManager
from datetime import date


class CustomManager(BaseUserManager):

    def create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError("Please Enter Email Address")
        if not password:
            raise ValueError("Please Enter Email Password")
        email = self.normalize_email(email)
        del extra_field["password1"]
        del extra_field["password2"]
        user = self.model(email=email, **extra_field)
        user.date_of_joined = date.today()
        user.login_date = date.today()
        user.logout_date = date.today()
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_field):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            **extra_field
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_users(self, email, password, **extra_field):
        return self.create_user(email, password, **extra_field)

