from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path("", views.PostListView.as_view(), name="list"),
    path("search/", views.post_search, name="search"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("create/", views.PostCreateView.as_view(), name="create"),
    path("update/<int:pk>/", views.PostUpdateView.as_view(), name="update"),
    # path("delete/<int:pk>/", views.PostDeleteView.as_view(), name="delete"),
    path("delete/<int:pk>/", views.delete, name="delete"),
    path("comment/", views.comment, name="comment"),
    path("user_posts/", views.user_posts, name="user_posts")
]
