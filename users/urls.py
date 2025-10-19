from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path("<int:pk>", views.ProfileView.as_view(), name="profile"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]