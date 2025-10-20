from django.db import models
from django.urls import reverse
from .utils import get_random_thumbnail


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        'users.User', related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)
    thumbnail = models.ImageField(
        upload_to='thumnails/', default=get_random_thumbnail)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-created_at"]


class Like(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user} likes {self.post}"
