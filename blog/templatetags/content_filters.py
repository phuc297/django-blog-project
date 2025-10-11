import random
from django import template

register = template.Library()


@register.filter
def truncate_words(content, n):
    """
    Returns the first n words of the given content.
    """
    words = content.split()
    return ' '.join(words[:n])


@register.filter
def random_truncate_words(content, n):
    n = random.randint(n-3, n+3)
    return truncate_words(content, n)
