from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # is_staff doubles as the admin flag for billing access
    pass
