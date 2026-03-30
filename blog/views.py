# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Category
from .forms import PostForm

POST_DETAIL = 'blog:post_detail'

def post_list(request):
    """Список всех опубликованных постов"""
    posts = Post.objects.filter(status='published').select_related('author', 'category')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, slug):
    """Детальная страница поста (только опубликованные)"""
    post = get_object_or_404(Post, slug=slug, status='published')
    return render(request, 'blog/post_detail.html', {'post': post})


def category_list(request):
    """Список категорий"""
    categories = Category.objects.annotate(
        post_count=Count('posts')
    ).filter(post_count__gt=0)
    return render(request, 'blog/category_list.html', {'categories': categories})


def posts_by_category(request, slug):
    """Посты по категории"""
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status='published')
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'category': category
    })


@login_required
def post_create(request):
    """Создание нового поста"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(POST_DETAIL, slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit(request, slug):
    """Редактирование поста (только автор)"""
    post = get_object_or_404(Post, slug=slug)
    
    if post.author != request.user:
        messages.error(request, 'Вы не можете редактировать этот пост')
        return redirect(POST_DETAIL, slug=post.slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(POST_DETAIL, slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {'form': form, 'post': post})


@login_required
def post_delete(request, slug):
    """Удаление поста (только автор)"""
    post = get_object_or_404(Post, slug=slug)
    
    if post.author != request.user:
        messages.error(request, 'Вы не можете удалить этот пост')
        return redirect('blog:post_list')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост удалён')
        return redirect('blog:post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def my_posts(request):
    """Мои посты"""
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})