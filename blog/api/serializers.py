from blog.models import Category, Tag, Article, Comment
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

        tags_serializer = TagSerializer(instance=instance.tags.all(), many=True)
        representation["tags"] = tags_serializer.data

        return representation


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    article = serializers.ReadOnlyField(source="article.title")

    class Meta:
        model = Comment
        fields = "__all__"
