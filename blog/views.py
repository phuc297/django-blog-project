import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView

from .forms import PostForm
from .models import Category, Post, Comment, Tag, Like


def post_search(request):
    # Lấy kiểu sắp xếp
    sort = request.GET.get("sort")
    sort = request.GET.get("sort") or "-created_at"

    tags = Tag.objects.all()
    categories = Category.objects.all()

    match sort:
        case "like":
            posts = Post.objects.annotate(
                num_likes=Count('like')
            ).order_by('-num_likes')
        case "comment":
            posts = Post.objects.annotate(
                num_cmts=Count('comments')
            ).order_by('-num_cmts')
        case _:
            posts = Post.objects.all().order_by(sort)

    # Tìm kiếm theo từ khóa
    search_query = request.GET.get("searchQuery", "")
    search_fields = request.GET.getlist("searchFields", ["title"])

    # Lấy thẻ và loại
    selected_tag = request.GET.get("tag", "all")
    selected_category = request.GET.get("category", "all")

    if search_query:
        q_filter = Q()
        if "title" in search_fields:
            q_filter |= Q(title__icontains=search_query)
        if "content" in search_fields:
            q_filter |= Q(content__icontains=search_query)
        if "author" in search_fields:
            q_filter |= Q(author__username__icontains=search_query)
        posts = posts.filter(q_filter).distinct()

        # Lọc theo thẻ và loại
        if selected_tag != 'all':
            posts = posts.filter(tags__name__icontains=selected_tag)

        if selected_category != 'all':
            posts = posts.filter(categories__name__icontains=selected_category)

    # Phân trang
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", "1")
    page_obj = paginator.get_page(page_number)

    return render(request=request,
                  template_name='blog/post_search.html',
                  context={'page_obj': page_obj,
                           'search_query': search_query,
                           'tags': tags,
                           'categories': categories,
                           'selected_tag': selected_tag,
                           'selected_category': selected_category,
                           'search_fields': search_fields, })


# View hiển thị danh sách bài viết
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


# View hiển thị chi tiết bài viết
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # Đếm số like và số bình luận
        context['like_count'] = post.like_set.count()
        context['comment_count'] = post.comments.count()
        if self.request.user.is_authenticated:
            context['user_liked'] = post.like_set.filter(
                user=self.request.user).exists()

        return context


# View tạo bài viết mới
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        print(form.instance.thumbnail.url)
        form.instance.author = self.request.user
        return super().form_valid(form)


# View cập nhật bài viết
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


# View xóa bài viết
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:user_posts')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


# View hiển thị danh sách bài viết của user
def user_posts(request):
    user = request.user

    # Lấy danh sách bài viết của user
    posts = Post.objects.filter(author=user).order_by('-created_at')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'user_profile': user,
    }
    return render(request, 'blog/user_post_list.html', context)


# API xóa bài viết
@login_required
def delete(request, pk):
    post = Post.objects.get(pk=pk)
    title = post.title
    if post.author.id != request.user.id:
        return JsonResponse({'thong bao': f'khong the xoa bai viet {title}'})
    post.delete()
    return JsonResponse({'thong bao': f'da xoa bai viet {title}'})


# API thích bài viết
@login_required
def like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        # Kiểm tra user đã like chưa
        liked = Like.objects.filter(post=post, user=user).exists()

        if liked:
            # Nếu đã like → bỏ like
            Like.objects.filter(post=post, user=user).delete()
            liked = False
        else:
            # Nếu chưa like → thêm like
            Like.objects.create(post=post, user=user)
            liked = True

        # Đếm lại tổng số like hiện tại
        like_count = post.like_set.count()

        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'like_count': like_count
        })
    else:
        return JsonResponse({'error': 'Request không hợp lệ'}, status=405)


# API bình luận vào bài viết
@login_required
def comment(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        content = data.get('content')
        post_id = data.get('post_id')
        post_id = int(post_id)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return JsonResponse({'error': 'Something went wrong'}, status=500)

    comment = Comment(content=content)
    comment.user = request.user
    comment.post = get_object_or_404(Post, pk=post_id)
    comment.save()

    formatted_created_at = str(
        comment.created_at.strftime('%b. %d, %Y, %I:%M %p'))

    return JsonResponse({'status': 'success',
                         'user': comment.user.username,
                         'avatar_url': comment.user.profile.avatar.url,
                         'created_at': formatted_created_at,
                         'content': comment.content,
                         },
                        status=201)
