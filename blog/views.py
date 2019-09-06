from django.shortcuts import render
from .models import Post


def post_list(request):
    post = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})
