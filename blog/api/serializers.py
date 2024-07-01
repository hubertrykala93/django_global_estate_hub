from blog.models import Category, Tag, Article, Comment
from accounts.models import User
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
    date_posted = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), help_text="Choose user.",
                                        required=False)
    title = serializers.CharField(max_length=1000, help_text="Type your article title.", required=False)
    image = serializers.ImageField(help_text="Choose image.", required=False)
    content = serializers.CharField(max_length=10000, help_text="Type your article content.", required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), help_text="Choose article category.",
                                                  required=False)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), help_text="Choose article tags.", many=True,
                                              required=False)

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
        read_only_fields = ["id", "date_posted", "slug"]

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)

        category_serializer = CategorySerializer(instance=instance.category)
        representation["category"] = category_serializer.data

        tag_serializer = TagSerializer(instance=instance.tags, many=True)
        representation["tags"] = tag_serializer.data

        return representation


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    date_posted = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    article = serializers.ReadOnlyField(source="article.title")
    article_id = serializers.ReadOnlyField(source="article.id")

    class Meta:
        model = Comment
        fields = "__all__"
