from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
  address= models.CharField(max_length=255, blank=True)
  phone_number = models.CharField(max_length=20, blank=True)
