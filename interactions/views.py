import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from blog.models import Post
from .models import Comment
from .forms import CommentForm


@login_required
def comment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = str(data.get('content'))
        post_id = int(data.get('post_id'))
        comment = Comment(content=content)
        comment.user = request.user
        comment.post = get_object_or_404(Post, pk=post_id)
        comment.save()
        formatted_created_at = str(comment.created_at.strftime('%b. %d, %Y, %I:%M %p'))
        print(formatted_created_at)
        return JsonResponse({'status': 'success',
                             'user': comment.user.username,
                             'avatar_url': comment.user.profile.avatar.url,
                             'created_at': formatted_created_at,
                             'content': comment.content,
                             },
                            status=201)

    return JsonResponse({'error': 'Invalid method'}, status=405)
