from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

class User(AbstractBaseUser):
    email = models.EmailField(('email address'), blank=False)       
    objects = UserManager()