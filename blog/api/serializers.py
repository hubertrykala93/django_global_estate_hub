from blog.models import Category, Tag, Article, Comment
from accounts.models import User
from accounts.api.serializers import UserSerializer
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    date_posted = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Article
        fields = [
            "id",
            "user",
            "image",
            "date_posted",
            "title",
            "content",
            "category",
            "tags",
            "slug",
        ]
        read_only_fields = ["id", "date_posted"]

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)

        category_serializer = CategorySerializer(instance=instance.category)
        representation["category"] = category_serializer.data

        return representation


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    date_posted = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    article = serializers.ReadOnlyField(source="article.title")
    article_id = serializers.ReadOnlyField(source="article.id")

    class Meta:
        model = Comment
        fields = "__all__"
