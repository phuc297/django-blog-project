from django.contrib import admin

from .models import Category, Tag, Post
from .models import Like, Comment

admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Comment)


class TagInline(admin.StackedInline):
    model = Post.tags.through
    extra = 1
    verbose_name = 'tag'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('categories', 'tags', 'created_at')
    inlines = [TagInline]
    exclude = ['tags',]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
