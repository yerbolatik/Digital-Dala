from django.db import models
from shortuuid.django_fields import ShortUUIDField

from userauths.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    category = models.ManyToManyField(
        Category, blank=True, related_name='posts')
    image = models.ImageField(upload_to='photos/', null=False, blank=False)
    description = models.TextField()
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else 'Post without title'

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_user")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    cid = ShortUUIDField(length=7, max_length=25,
                         alphabet='abcdefghijklmnopqrstuvwxyz')

    def __str__(self):
        if self.post:
            return f'Comment on {self.post.title if self.post.title else "untitled post"}'
        elif self.news:
            return f'Comment on {self.news.title}'
        else:
            return 'Comment'
