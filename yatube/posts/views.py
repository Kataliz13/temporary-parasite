from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Group, Post, User
from .utils import paginator


def index(request):
    posts = Post.objects.select_related('author', 'group')
    template = 'posts/index.html'
    context = {
        'page_obj': paginator(posts, request),
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.groups.select_related('author')
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': paginator(posts, request)
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('group')
    template = 'posts/profile.html'
    context = {
        'author': author,
        'page_obj': paginator(posts, request),
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    form = CommentForm()
    comments = post.comments.all()
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'author': author,
        'form': form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', post.author)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    template = "posts/create_post.html"
    if not request.user == post.author:
        return redirect("posts:post_detail", post_id)
    if form.is_valid() and request.method == "POST":
        post = form.save()
        return redirect("posts:post_detail", post_id)
    context = {
        "form": form,
        "is_edit": True,
        "post": post,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)
