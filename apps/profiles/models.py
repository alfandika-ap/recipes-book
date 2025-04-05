from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel


# Create your models here.
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
