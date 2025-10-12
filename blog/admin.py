from django.contrib import admin
from .models import Category, Tag, Post
from .models import Like, Comment


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
