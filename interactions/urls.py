from django.urls import path

from . import views

app_name = 'interactions'
urlpatterns = [
    path("comment/", views.comment, name="comment")
]
