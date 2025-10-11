from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path("", views.post_list, name="list"),
    path("<int:post_id>/", views.post_detail, name="detail"),
    path("create/", views.PostCreateView.as_view(), name="create"),
    
]
