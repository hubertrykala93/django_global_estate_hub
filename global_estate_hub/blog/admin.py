from django.contrib import admin
from .models import Category, Tag, Article, Comment


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_editable = ['slug']
    list_filter = ['name']
    prepopulated_fields = {
        'slug': ['name']
    }
    list_display_links = ['name']


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    list_display_links = ['name']


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    fields = ['user', 'title', 'category', 'image', 'date_posted', 'content', 'slug', 'tags']
    list_display = ['user', 'title', 'category', 'image', 'date_posted', 'slug']
    list_filter = ['user', 'category', 'date_posted', 'tags']
    list_editable = ['image', 'category']
    list_display_links = ['title']
    prepopulated_fields = {'slug': ['title']}


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email', 'date_posted', 'content', 'likes', 'dislikes', 'active']
    list_filter = ['user', 'full_name', 'email', 'date_posted', 'active']
    list_editable = ['full_name', 'email', 'content', 'active']
    list_display_links = ['user']
