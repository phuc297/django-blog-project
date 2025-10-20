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
