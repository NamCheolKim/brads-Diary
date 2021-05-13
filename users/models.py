from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    """Custom User Model Definition"""

    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
