from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path("<int:pk>", views.ProfileView.as_view(), name="profile"),
    path("<int:user_id>/posts/", views.user_posts, name="posts"),
    path("follow/", views.follow, name="follow"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]