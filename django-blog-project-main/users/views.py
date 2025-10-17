from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from .forms import HomeForm, RegisterForm, LoginForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # đăng nhập luôn sau khi đăng ký
            return redirect("home")  # đổi "home" thành tên url bạn muốn
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse("blog:page"))  # đổi "home" thành tên url bạn muốn
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("users:login")
def HomeView(request):
    form = HomeForm()
    return render(request, "users/page.html", {'form': form})

def hscn(request):
    return render(request, "users/hscn.html")
def changpw(request):
    return render(request, "users/changepw.html")