from django.contrib import admin
from .models import User, Profile

admin.site.register(User)


class ProfileAdmin(admin.ModelAdmin):
    fields = ['bio', 'avatar', 'following']


admin.site.register(Profile, ProfileAdmin)
