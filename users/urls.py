from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'
urlpatterns = [
    path("<int:pk>", views.ProfileView.as_view(), name="profile"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("follow/", views.follow, name="follow"),
    path("<int:user_id>/posts/", views.user_posts, name="posts"),
    path("edit_profile/", views.edit_profile_view, name="edit_profile"),

    # Password change using Django's built-in views
    path('password/change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
]