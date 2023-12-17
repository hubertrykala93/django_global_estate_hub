from django.contrib import admin
from .models import Category, Tag, Article, Comment
from django.utils.translation import ngettext
from django.contrib import messages


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
    list_display = ['name', 'slug']
    list_filter = ['name']
    list_display_links = ['name']
    prepopulated_fields = {'slug': ['name']}


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    ordering = ['date_posted']
    fields = ['user', 'title', 'category', 'image', 'date_posted', 'content', 'slug', 'tags']
    list_display = ['user', 'title', 'category', 'image', 'date_posted', 'slug']
    list_filter = ['user', 'category', 'date_posted', 'tags']
    list_editable = ['image', 'category']
    list_display_links = ['title']
    prepopulated_fields = {'slug': ['title']}


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'date_posted', 'comment', 'likes', 'dislikes', 'active']
    list_filter = ['user', 'full_name', 'date_posted', 'active']
    list_editable = ['active']
    list_display_links = ['user']
    actions = ['approve_comment']

    @admin.action(description='Approve selected Comments')
    def approve_comment(self, request, queryset):
        updated = queryset.update(active=True)

        self.message_user(request=request,
                          message=ngettext(singular=f'{updated} comment has been approved successfully.',
                                           plural=f'{updated} comments have been approved successfully.',
                                           number=updated),
                          level=messages.SUCCESS)
