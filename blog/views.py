from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostForm


def post_share(request, post_id):
    # TODO REMOVE
    print("YUHU!" + request)
    # Retrieve by post id
    post = get_object_or_404(Post, id=post_id, status='Published')
    send = false

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form passes validation
            cd = form.cleaned_data
            # send email
            # post_url = request.build_absolute_uri(post.get_absolute_url())
            # subject = '{} ({}) recommends you reading "{}"'.format(
            #     cd['name'], cd['email'], post.title)
            # message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
            #     post.title, post_url, cd['name'], cd['comments'])
            # send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            # sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {
        'post': post,
        'form': form,
        'sent': sent,
    })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
    )
    return render(request, 'blog/post/detail.html', {'post': post})


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 post per page
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page results
        post = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {
        'page': page,
        'posts': post
    })


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
