from django.dispatch import Signal, receiver
from user.models import CustomUser
import datetime

Login_User = Signal()
Logout_User = Signal()


@receiver(Login_User)
def login_user_handler(sender, **kwargs):
    login_time = datetime.datetime
    user = CustomUser.objects.get(email=sender)
    user.login_date = login_time.today()
    user.save()


@receiver(Logout_User)
def logout_user_handler(sender, **kwargs):
    logout_time = datetime.datetime
    user = CustomUser.objects.get(email=sender)
    user.logout_date = logout_time.today()
    user.save()
