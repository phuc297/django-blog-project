import json
from .models import Category, Post, Comment, Tag
from users.models import User
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count


def post_search(request):

    # Lấy kiểu sắp xếp
    sort = (request.GET.get("sort") or "-created_at").strip()

    if not sort:
        sort = '-created_at'
    else:
        allowed_sorts = ["created_at", "-created_at", "like", "comment"]
        if sort not in allowed_sorts:
            sort = "-created_at"

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
    searchQuery = (request.GET.get("searchQuery") or "").strip()

    # Lấy thẻ và loại 
    selected_tag = (request.GET.get("tag") or "all").strip()
    selected_category = (request.GET.get("category") or "all").strip()

    if (not selected_tag):
        selected_tag = 'all'

    if selected_tag != 'all':
        posts = posts.filter(tags__name__icontains=selected_tag)

    if (not selected_category):
        selected_category = 'all'

    if selected_category != 'all':
        posts = posts.filter(categories__name__icontains=selected_category)

    if searchQuery:
        posts = posts.filter(title__icontains=searchQuery)

    # Phân trang
    paginator = Paginator(posts, 10)
    page_number = (request.GET.get("page") or "1").strip()
    page_obj = paginator.get_page(page_number)

    return render(request=request,
                  template_name='blog/post_search.html',
                  context={'page_obj': page_obj,
                           'searchQuery': searchQuery,
                           'tags': tags,
                           'categories': categories,
                           'selected_tag': selected_tag,
                           'selected_category': selected_category})


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

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


# API xóa bài viết
@login_required
def delete(request, pk):
    post = Post.objects.get(pk=pk)
    title = post.title
    if post.author.id != request.user.id:
        return JsonResponse({'thong bao': f'khong the xoa bai viet {title}'})
    post.delete()
    return JsonResponse({'thong bao': f'da xoa bai viet {title}'})


# View hiển thị danh sách bài viết của user
def user_posts(request):
    return render(request, 'blog/user_post_list.html')


# API bình luận vào bài viết
@login_required
def comment(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        content = data.get('content')
        post_id = data.get('post_id')

        if not content or post_id is None:
            return JsonResponse({'error': 'Missing content or post_id'}, status=400)

        post_id = int(post_id)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Cannot load JSON data'}, status=400)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid post_id'}, status=400)
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
