from django.shortcuts import redirect, render
from django.urls import reverse

from django.views.generic import DetailView, UpdateView

from users.forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from .models import Profile


class ProfileView(DetailView):
    model = Profile
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    

# Trang chỉnh sửa profile
# class ProfileUpdateView(UpdateView):
#     model = Profile
#     template_name = 'users/profile_forms.html'
    


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("users:login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse("blog:list"))
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("users:login")
