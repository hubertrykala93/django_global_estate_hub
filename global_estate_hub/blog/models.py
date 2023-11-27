from django.db import models
from accounts.models import User
from django.utils.timezone import now
from django.shortcuts import reverse
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    """
    Creating Category model instance.
    """
    name = models.CharField(max_length=50, choices=[
        ('Apartment', 'Apartment'),
        ('Family House', 'Family House'),
        ('Luxury Villa', 'Luxury Villa'),
        ('Manufactured Home', 'Manufactured Home'),
        ('Rentals', 'Rentals'),
        ('Buys', 'Buys'),
    ])

    slug = models.SlugField(max_length=50, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """
        Returns the string representation of the category's name and displays it in the administrator panel.

        return: str
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the absolute URL for a given category.

        return HttpsResponseRedirect
        """
        return reverse(viewname='article-categories', kwargs={
            'category_slug': self.slug,
        })


class Tag(models.Model):
    """
    Creating Tag model instance.
    """
    tag = models.CharField(max_length=50, choices=[
        ('Apartment', 'Apartment'),
        ('Business', 'Business'),
        ('Real Estate', 'Real Estate'),
        ('Popular', 'Popular'),
        ('Luxury Villa', 'Luxury Villa'),
        ('Design', 'Design')
    ])

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        """
        Returns the string representation of the tag's name and displays it in the administrator panel.

        return: str
        """
        return self.tag


class Article(models.Model):
    """
    Creating Article model instance.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article_images')
    date_posted = models.DateTimeField(default=now)
    title = models.CharField(max_length=200, unique=True)
    content = RichTextUploadingField(max_length=10000, unique=True)
    category = models.ForeignKey(to=Category, related_name='article', on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(to=Tag)
    slug = models.SlugField(max_length=200, unique=True, null=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['date_posted']

    def __str__(self):
        """
        Returns the string representation of the article's title and displays it in the administrator panel.

        return: str
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the absolute URL for a given article.

        return HttpsResponseRedirect
        """
        return reverse(viewname='article-details', kwargs={
            'category_slug': self.category.slug,
            'article_slug': self.slug,
        })

    def save(self, *args, **kwargs):
        """
        Converts the article's image to a smaller size based on proportions.

        return: None
        """
        super(Article, self).save(*args, **kwargs)

        img = Image.open(fp=self.image.path)

        if img.mode == 'RGBA':
            img.convert(mode='RGB')

        img_width = img.width
        img_height = img.height

        output_width = 1100
        output_height = img_height * output_width / img_width

        img.thumbnail(size=(output_width, output_height))
        img.save(fp=self.image.path)


class Comment(models.Model):
    """
    Creating Comment model instance.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    date_posted = models.DateTimeField(default=now)
    content = models.TextField(max_length=1000)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        """
        Returns the string representation of the fullname of the user who commented on a given article
        and displays it in the administrator panel.

        return: str
        """
        return f'{self.full_name} comment.'
