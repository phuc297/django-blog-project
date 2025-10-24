import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from django.views.generic import DetailView, UpdateView
from django.contrib.auth.decorators import login_required

from users.forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from .models import Profile, User
from django.db.models import Count
from django.core.paginator import Paginator

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from users.forms import RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate, logout
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect


class ProfileView(DetailView):
    model = Profile
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        paginator = Paginator(obj.user.posts.all(), 9)
        page_obj = paginator.get_page('1')

        is_following = False
        if self.request.user.is_authenticated and self.request.user.id != obj.id:
            try:
                is_following = obj in self.request.user.profile.following.all()
            except Profile.DoesNotExist:
                pass

        context['page_obj'] = page_obj
        context['is_following'] = is_following
        return context


# Trang chỉnh sửa profile
# class ProfileUpdateView(UpdateView):
#     model = Profile
#     template_name = 'users/profile_forms.html'


@login_required
def follow(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        profile_id = data.get('profile_id')
    except Exception as e:
        print(f"Unexpected error: {e}")
        return JsonResponse({'error': 'Something went wrong when loading json data'}, status=500)

    try:
        profile: Profile = request.user.profile
        followed_profile = get_object_or_404(Profile, pk=profile_id)
        if followed_profile in profile.following.all():
            profile.following.remove(followed_profile)
        else:
            profile.following.add(followed_profile)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return JsonResponse({'error': 'Something went wrong'}, status=500)

    return JsonResponse({'status': 'success'}, status=201)


def user_posts(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = user.posts

    sort = request.GET.get('sort', 'newest')

    if sort == 'popular':
        posts = posts.annotate(
            num_cmts=Count('comments')
        ).order_by('-num_cmts')
    else:
        posts = posts.order_by('-created_at')

    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/partials/posts.html', {'page_obj': page_obj,
                                                         'user_id': user_id})


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


def edit_profile_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('users:login')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user.profile)
        password_form = PasswordChangeForm(user, request.POST)

        # Which submit button was pressed?
        if 'password_submit' in request.POST:
            if password_form.is_valid():
                user_obj = password_form.save()
                update_session_auth_hash(request, user_obj)
                return redirect('users:password_change_done')
        else:
            # profile submit (either user_form or profile_form). We accept partial updates.
            valid_user = user_form.is_valid()
            valid_profile = profile_form.is_valid()
            if valid_user and valid_profile:
                user_form.save()
                profile_form.save()
                return redirect('users:profile', pk=user.pk)
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user.profile)
        password_form = PasswordChangeForm(user)

    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'profile': user.profile,
    })


def change_password(request):
    if request.method == 'POST':
        # Form này yêu cầu request.user
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()  # Tự động gọi set_password và save

            # Quan trọng: Cập nhật session để người dùng không bị logout
            update_session_auth_hash(request, user)

            print("Đổi mật khẩu thành công!")
            return redirect('profile')  # Chuyển hướng về trang profile
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})
