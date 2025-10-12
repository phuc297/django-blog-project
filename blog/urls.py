from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path("", views.post_list, name="list"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("create/", views.PostCreateView.as_view(), name="create"),
    path("comment/", views.comment, name="comment")
    
]
