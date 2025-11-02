from django import template

from users.models import Profile

register = template.Library()


@register.filter
def is_following(user, author):
    if not user.is_authenticated:
        return False

    try:
        return author.profile in user.profile.following.all()
    except Profile.DoesNotExist:
        pass

    return False
