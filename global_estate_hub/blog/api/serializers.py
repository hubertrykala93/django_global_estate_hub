from blog.models import Category, Tag, Article, Comment, CommentLike, CommentDislike
from rest_framework import serializers
from accounts.api.serializers import UserSerializer, UserUsernameSerializer


class CategorySerializer(serializers.Serializer):
    """
    Category Model Serializer.
    """
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    slug = serializers.SlugField()

    class Meta:
        model = Category


class TagSerializer(serializers.Serializer):
    """
    Tag Model Serializer.
    """
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    slug = serializers.SlugField()

    class Meta:
        model = Tag


class ArticleSerializer(serializers.Serializer):
    """
    Article Model Serializer.
    """
    id = serializers.ReadOnlyField
    user = UserSerializer()
    image = serializers.ImageField()
    date_posted = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    title = serializers.CharField()
    content = serializers.CharField()
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    slug = serializers.SlugField()

    class Meta:
        model = Article


class ArticleTitleSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField()

    class Meta:
        model = Article


class CommentSerializer(serializers.Serializer):
    """
    Comment Model Serializer.
    """
    id = serializers.ReadOnlyField()
    user = UserUsernameSerializer()
    article = ArticleTitleSerializer()
    full_name = serializers.CharField()
    date_posted = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    comment = serializers.CharField()
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()
    # parent = serializers.SerializerMethodField(read_only=True, method_name='get_children_comments')
    active = serializers.BooleanField()

    class Meta:
        model = Comment
