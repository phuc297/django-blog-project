from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

