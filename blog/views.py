from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post
from blog.models import Tag
from blog.models import Category

def index(request):
    # return HttpResponse('index')
    return render(request=request, template_name='index/index.html')

def post_list(request):

    #Lấy kiểu sắp xếp
    sort = request.GET.get("sort")

    if not sort:
        sort = '-created_at'

    tags = Tag.objects.all()
    categories = Category.objects.all()
    posts = Post.objects.all().order_by(sort)

    #Tìm kiếm theo từ khóa
    searchQuery = request.GET.get("searchQuery")

    #Lấy thẻ và loại
    selected_tag = request.GET.get("tag")
    selected_category = request.GET.get("category")

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

    #Phân trang
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request=request, template_name='blog/post_list.html', context= {'page_obj': page_obj,
                                                                                  'searchQuery': searchQuery,
                                                                                  'tags' : tags,
                                                                                  'categories' : categories,
                                                                                  'selected_tag' : selected_tag,
                                                                                  'selected_category' : selected_category})

def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render(request=request, template_name='blog/post_detail.html', context= {'post': post})
