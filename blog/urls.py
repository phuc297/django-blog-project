from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path("", views.post_list, name="home"),
    path("<int:post_id>/", views.post_detail, name="detail"),
    
]
