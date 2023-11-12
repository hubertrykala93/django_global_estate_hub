from django.db import models
from accounts.models import User
from django.utils.timezone import now


class Category(models.Model):
    category = models.CharField(max_length=50, choices=[
        ('Apartment', 'Apartment'),
        ('Family House', 'Family House'),
        ('Luxury Villa', 'Luxury Villa'),
        ('Manufactured Home', 'Manufactured Home'),
        ('Rentals', 'Rentals'),
        ('Buys', 'Buys'),
    ])

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category


class Tag(models.Model):
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
        return self.tag


class Article(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article_images')
    date_posted = models.DateTimeField(default=now)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    categories = models.ManyToManyField(to=Category)
    tags = models.ManyToManyField(to=Tag)
    slug = models.SlugField(max_length=200, null=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    date_posted = models.DateTimeField(default=now)
    content = models.TextField(max_length=1000)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.content
