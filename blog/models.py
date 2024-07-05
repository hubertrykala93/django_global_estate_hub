from django.db import models
from accounts.models import User
from django.utils.timezone import now
from django.shortcuts import reverse
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import TreeForeignKey, MPTTModel
from uuid import uuid4


class Category(models.Model):
    """
    Creating Category model instance.
    """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(
        max_length=50,
        choices=[
            ("Apartment", "Apartment"),
            ("Family House", "Family House"),
            ("Luxury Villa", "Luxury Villa"),
            ("Manufactured Home", "Manufactured Home"),
            ("Rentals", "Rentals"),
            ("Buys", "Buys"),
        ],
    )

    slug = models.SlugField(max_length=100, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        """
        Returns the string representation of the category's name and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.name

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL for a given category.

        Returns
        ----------
            str
        """
        return reverse(
            viewname="article-categories",
            kwargs={
                "category_slug": self.slug,
            },
        )


class Tag(models.Model):
    """
    Creating Tag model instance.
    """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self) -> str:
        """
        Returns the string representation of the tag's name and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.name

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL for a given tag.

        Returns
        ----------
            str
        """
        return reverse(
            viewname="article-tags",
            kwargs={
                "tag_slug": self.slug,
            },
        )


class Article(models.Model):
    """
    Creating Article model instance.
    """

    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="article_images")
    date_posted = models.DateTimeField(default=now)
    title = models.CharField(max_length=200, unique=True)
    content = RichTextUploadingField(max_length=10000, unique=True, blank=True)
    category = models.ForeignKey(
        to=Category, related_name="article", on_delete=models.CASCADE, null=True
    )
    tags = models.ManyToManyField(to=Tag, related_name="tags")
    slug = models.SlugField(max_length=200, unique=True, null=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["date_posted"]

    def __str__(self):
        """
        Returns the string representation of the article's title and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.title

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL for a given article.

        Returns
        ----------
            str
        """
        return reverse(
            viewname="article-details",
            kwargs={
                "category_slug": self.category.slug,
                "article_slug": self.slug,
            },
        )

    def save(self, *args, **kwargs):
        """
        Converts the article's image to a smaller size based on proportions.

        Parameters
        ----------
            args: tuple
            kwargs: dict

        Returns
        ----------
            None
        """
        super(Article, self).save(*args, **kwargs)

        img = Image.open(fp=self.image.path)

        if img.mode == "RGBA":
            img.convert(mode="RGB")

        img_width = img.width
        img_height = img.height

        output_width = 1100
        output_height = img_height * output_width / img_width

        img.thumbnail(size=(output_width, output_height))
        img.save(fp=self.image.path)

    @property
    def rename_image(self) -> str:
        """
        Returns new name of uploaded user profile image.

        Returns:
        ----------
            str
        """
        return f"{uuid4()}" + f".{self.image.path.split(sep='.')[-1]}"


class Comment(MPTTModel):
    """
    Creating Comment model instance.
    """

    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments",
    )
    article = models.ForeignKey(
        to=Article, on_delete=models.CASCADE, null=True, related_name="comments"
    )
    full_name = models.CharField(max_length=200, blank=True, null=True)
    date_posted = models.DateTimeField(default=now)
    comment = models.TextField(max_length=1000)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    parent = TreeForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    class MPTTMeta:
        order_insertion_by = ["date_posted"]

    def __str__(self):
        """
        Returns a string representation of the comment ID that is the parent.
        """
        return f"{self.id}"


class CommentLike(models.Model):
    """
    Creating CommentLike model instance.
    """

    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="comment_like"
    )
    comment = models.ForeignKey(
        to=Comment, on_delete=models.CASCADE, related_name="comment_like"
    )

    class Meta:
        verbose_name = "Comment Like"
        verbose_name_plural = "Comment Likes"

    def __str__(self) -> str:
        """
        Returns a string representation of the user giving a Like,
        along with the comment content, and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return f"{self.user}, {self.comment}"


class CommentDislike(models.Model):
    """
    Creating CommentDislike model instance.
    """

    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="comment_dislike"
    )
    comment = models.ForeignKey(
        to=Comment, on_delete=models.CASCADE, related_name="comment_dislike"
    )

    class Meta:
        verbose_name = "Comment Dislike"
        verbose_name_plural = "Comment Dislikes"

    def __str__(self) -> str:
        """
        Returns a string representation of the user giving a Dislike,
        along with the comment content, and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return f"{self.user}, {self.comment}"
