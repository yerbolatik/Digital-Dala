from django.contrib import admin
from core.models import Category, Post, Comment, News

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(News)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category',
                    'image', 'description', 'likes', 'pdf']
    list_filter = ['category']
    search_fields = ['title', 'description']
