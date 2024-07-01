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
    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        help_text="Select the article author.",
        required=False
    )
    title = serializers.CharField(
        max_length=1000,
        help_text="Enter the article title.",
        required=False
    )
    image = serializers.ImageField(
        help_text="Upload the main article image.",
        required=False
    )
    content = serializers.CharField(
        max_length=10000,
        help_text="Enter the article content.",
        required=False
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        help_text="Select the article category.",
        required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        help_text="Select at least one tag.",
        many=True,
        required=False
    )

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

    def validate_title(self, title):
        if title is None:
            raise serializers.ValidationError(detail="The title field cannot be empty.")

        if title and len(title) < 10:
            raise serializers.ValidationError(detail="The title must be at least 10 characters long.")

        if title and len(title) >= 10 and Article.objects.filter(title=title).exists():
            raise serializers.ValidationError(detail="The given article title already exists.")

        return title

    def validate_image(self, image):
        if image is None:
            raise serializers.ValidationError(detail="The image field cannot be empty.")

        if image and image.name.split('.')[1] not in ["jpg", "jpeg", "png", "svg", "webp"]:
            raise serializers.ValidationError(
                detail="Invalid file format. Allowed formats are 'jpg', 'jpeg', 'png', 'svg', 'webp'.")

        return image

    def validate_content(self, content):
        if content is None:
            raise serializers.ValidationError(detail="The content field cannot be empty.")

        if content and len(content) < 10:
            raise serializers.ValidationError(detail="The content must be at least 10 characters long.")

        return content

    def validate_tags(self, tags):
        if len(tags) == 0:
            raise serializers.ValidationError(detail="You must select at least one tag.")

        return tags


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    date_posted = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    article = serializers.ReadOnlyField(source="article.title")
    article_id = serializers.ReadOnlyField(source="article.id")

    class Meta:
        model = Comment
        fields = "__all__"
