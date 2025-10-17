from django.http import HttpResponse
from django.shortcuts import render

from blog.models import Post

def index(request):
    # return HttpResponse('index')
    return render(request=request, template_name='index/index.html')

def post_list(request):
    posts = Post.objects.all()
    return render(request=request, template_name='blog/post_list.html', context= {'posts': posts})

def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render(request=request, template_name='blog/post_detail.html', context= {'post': post})


