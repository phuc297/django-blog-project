from interactions.forms import CommentForm
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse('index')
    return render(request=request, template_name='index/index.html')


def post_list(request):
    posts = Post.objects.all()
    return render(request=request, template_name='blog/post_list.html', context={'posts': posts})


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = CommentForm
    return render(request=request, template_name='blog/post_detail.html', context={'post': post, 'form': form})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):  # Gán tác giả là user hiện tại trước khi lưu
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
