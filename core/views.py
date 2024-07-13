from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from core.forms import PostForm

from core.models import Post, Comment, Category, News
from userauths.models import User


def index(request):
    categories = Category.objects.all()
    posts = Post.objects.all()
    news_list = News.objects.all()
    context = {
        'categories': categories,
        'posts': posts,
        'news': news_list
    }
    return render(request, 'core/index.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'core/index.html'
    paginate_by = 5
    title = 'Категории'

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data()
        context['title'] = 'Категории'
        context['categories'] = Category.objects.all()
        context['current_category'] = Category.objects.get(
            id=self.kwargs.get('category_id')) if self.kwargs.get('category_id') else None
        return context


def author(request):
    authors = User.objects.filter(is_author=True)

    context = {
        "authors": authors,
    }
    return render(request, "core/authors.html", context)


def author_detail(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(active=True, user=author).order_by("-id")

    context = {
        "author": author,
        "posts": posts,
    }
    return render(request, "core/author_detail.html", context)


@login_required
@require_POST
def create_post(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        form.save_m2m()  # Для сохранения связей Many-to-Many
        if not request.user.is_author:
            request.user.is_author = True
            request.user.save()
        return redirect('core:index')
    return render(request, 'core/add_post.html', {'form': form})


def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug)
    context = {'news_item': news_item}
    return render(request, 'core/news_detail.html', context)


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'core/post_detail.html', {'post': post})


# def registration_view(request):
#     return render(request, 'core/registration.html')


# def photo_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     comments = post.comments.all()
#     return render(request, 'core/photo_detail.html', {'post': post, 'comments': comments})


@csrf_exempt
def like_photo(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        post.likes += 1
        post.save()
        return JsonResponse({'likes': post.likes})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def like_news(request, pk):
    if request.method == 'POST':
        news_item = get_object_or_404(News, pk=pk)
        news_item.likes += 1
        news_item.save()
        return JsonResponse({'likes': news_item.likes})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def add_comment(request, pk):
    if request.method == 'POST':
        post = Post.objects.filter(pk=pk).first()
        news_item = News.objects.filter(pk=pk).first()
        comment_text = request.POST.get('text')
        if comment_text:
            if post:
                Comment.objects.create(post=post, text=comment_text)
                comments = post.comments.values('text', 'created_at')
            elif news_item:
                Comment.objects.create(news=news_item, text=comment_text)
                comments = news_item.comments.values('text', 'created_at')
            else:
                return JsonResponse({'error': 'Invalid request'}, status=400)
            return JsonResponse({'comments': list(comments)})
    return JsonResponse({'error': 'Invalid request'}, status=400)
