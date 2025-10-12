from django.db import models
from django.contrib.auth.models import AbstractUser

from .utils import get_random_avatar



class User(AbstractUser):
    email = models.EmailField(unique=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default=get_random_avatar)
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers')
    
    def __str__(self):
        return str(self.user)

