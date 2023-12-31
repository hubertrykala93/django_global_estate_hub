from django.contrib import admin
from .models import Category, Tag, Article, Comment, CommentLike, CommentDislike
from django.utils.translation import ngettext
from django.contrib import messages
from mptt.admin import MPTTModelAdmin


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    """
    Admin options and functionalities for Category model.
    """
    list_display = ['id', 'name', 'slug']
    list_editable = ['slug']
    list_filter = ['name']
    prepopulated_fields = {
        'slug': ['name']
    }
    list_display_links = ['name']
    search_fields = ['name']
    ordering = ['name']
    fieldsets = [
        [
            'Category Name:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'Category Alias:', {
            'fields': [
                'slug',
            ]
        }
        ]
    ]


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    """
    Admin options and functionalities for Tag model.
    """
    list_display = ['id', 'name', 'slug']
    list_filter = ['name']
    list_display_links = ['name']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']
    ordering = ['name']
    fieldsets = [
        [
            'Tag Name:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'Tag Alias:', {
            'fields': [
                'slug',
            ]
        }
        ]
    ]


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    """
    Admin options and functionalities for Article model.
    """
    list_display = ['id', 'user', 'title', 'category', 'image', 'date_posted', 'slug', 'get_tags']
    list_filter = ['user', 'category', 'date_posted', 'tags']
    list_editable = ['user', 'image', 'category']
    list_display_links = ['title']
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title']
    ordering = ['date_posted']
    fieldsets = [
        [
            'Creator:', {
            'fields': [
                'user',
            ]
        }
        ],
        [
            'Image:', {
            'fields': [
                'image',
            ]
        }
        ],
        [
            'Date Posted:', {
            'fields': [
                'date_posted',
            ]
        }
        ],
        [
            'Content:', {
            'fields': [
                'title',
                'content',
            ]
        }
        ],
        [
            'Alias:', {
            'fields': [
                'slug',
            ]
        }
        ],
        [
            'Category:', {
            'fields': [
                'category',
            ]
        }
        ],
        [
            'Tags:', {
            'fields': [
                'tags',
            ]
        }
        ]
    ]

    @admin.display(description='Tags')
    def get_tags(self, obj):
        """
        Displays in the admin panel all tags assigned to a given article.

        return: str
        """
        return '\n'.join([tag.name for tag in obj.tags.all()])


@admin.register(Comment)
class AdminComment(MPTTModelAdmin):
    """
    Admin options and functionalities for Comment model.
    """
    list_display = ['id', 'user', 'article', 'full_name', 'date_posted', 'comment', 'likes', 'dislikes', 'active',
                    'parent']
    list_filter = ['user', 'full_name', 'date_posted', 'likes', 'dislikes', 'active']
    list_editable = ['likes', 'dislikes', 'active']
    list_display_links = ['user']
    actions = ['approve_comments']
    search_fields = ['user', 'comment']
    ordering = ['date_posted']
    fieldsets = [
        [
            'Creator:', {
            'fields': [
                'user',
                'full_name',
            ]
        }
        ],
        [
            'Date:', {
            'fields': [
                'date_posted',
            ]
        }
        ],
        [
            'Related to:', {
            'fields': [
                'article',
            ]
        }
        ],
        [
            'Status:', {
            'fields': [
                'active',
            ]
        }
        ],
        [
            'Content', {
            'fields': [
                'comment',
            ]
        }
        ],
        [
            'Rates:', {
            'fields': [
                'likes',
                'dislikes',
            ]
        }
        ],
        [
            'Parent to:', {
            'fields': [
                'parent',
            ]
        }
        ]
    ]

    @admin.action(description='Approve selected Comments')
    def approve_comments(self, request, queryset):
        """
        Approves all selected comments that have the 'active' attribute set to 'False'.

        return: None
        """
        updated = queryset.update(active=True)

        self.message_user(request=request,
                          message=ngettext(singular=f'{updated} comment has been approved successfully.',
                                           plural=f'{updated} comments have been approved successfully.',
                                           number=updated),
                          level=messages.SUCCESS)


@admin.register(CommentLike)
class AdminCommentLike(admin.ModelAdmin):
    """
    Admin options and functionalities for CommentLike model.
    """
    list_display = ['id', 'user', 'comment']
    list_filter = ['user', 'comment']
    list_display_links = ['user']
    search_fields = ['user', 'comment']
    ordering = ['user']
    fieldsets = [
        [
            'User:', {
            'fields': [
                'user',
            ]
        }
        ],
        [
            'Comment:', {
            'fields': [
                'comment',
            ]
        }
        ]
    ]


@admin.register(CommentDislike)
class AdminCommentDislike(admin.ModelAdmin):
    """
    Admin options and functionalities for CommentDislike model.
    """
    list_display = ['id', 'user', 'comment']
    list_filter = ['user', 'comment']
    list_display_links = ['user']
    search_fields = ['user', 'comment']
    ordering = ['user']
    fieldsets = [
        [
            'User:', {
            'fields': [
                'user',
            ]
        }
        ],
        [
            'Comment:', {
            'fields': [
                'comment',
            ]
        }
        ]
    ]
