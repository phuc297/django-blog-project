import json
from .models import Post, Comment
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required


def index(request):
    # return HttpResponse('index')
    return render(request=request, template_name='index/index.html')


def post_list(request):
    posts = Post.objects.all()
    return render(request=request, template_name='blog/post_list.html', context={'posts': posts})


# def post_detail(request, post_id):
#     post = Post.objects.get(pk=post_id)
#     return render(request=request, template_name='blog/post_detail.html', context={'post': post})

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


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
