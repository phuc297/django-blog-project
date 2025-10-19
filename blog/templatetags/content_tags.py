import random
from django import template
from django.db.models import Count
from blog.models import Category, Post, Tag
from users.models import User

register = template.Library()


@register.inclusion_tag('blog/partials/top_posts.html')
def top_posts(count=3):
    posts = Post.objects.order_by('-created_at')[:count]
    return {'posts': posts}


@register.inclusion_tag('blog//partials/top_authors.html')
def top_authors(count=5):
    authors = User.objects.annotate(
        post_count=Count('posts')).order_by('-post_count')[:count]
    return {'authors': authors}


@register.inclusion_tag('blog//partials/top_categories.html')
def top_categories(count=5):
    categories = Category.objects.all()[:count]
    return {'categories': categories}


@register.inclusion_tag('blog//partials/top_tags.html')
def top_tags(count=5):
    tags = Tag.objects.all()[:count]
    return {'tags': tags}
