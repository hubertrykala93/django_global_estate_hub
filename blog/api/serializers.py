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
    image = serializers.SerializerMethodField(method_name="get_image_name")

    class Meta:
        model = Article
        fields = [
            "id",
            "user",
            "date_posted",
            "title",
            "slug",
            "image",
            "content",
            "category",
            "tags",
        ]
        extra_kwargs = {
            "date_posted": {
                "format": "%Y-%m-%d %H:%M:%S",
                "read_only": True,
            }
        }

    def get_image_name(self, obj):
        return obj.image.name.split("/")[-1]


class ArticleCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text="Select the article author.",
        required=True,
        allow_null=True,
    )
    title = serializers.CharField(max_length=1000, help_text="Enter the article title.",
                                  allow_blank=True)
    content = serializers.CharField(max_length=100000, help_text="Enter the article content.",
                                    allow_blank=True)
    image = serializers.ImageField(help_text="Upload the main article image.", allow_null=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        help_text="Select the article category.",
        allow_null=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        help_text="Select at least one tag.",
        many=True,
        allow_null=True,
    )

    class Meta:
        model = Article
        fields = [
            "id",
            "user",
            "title",
            "content",
            "image",
            "category",
            "tags",
            "slug",
        ]
        read_only_fields = ["id", "slug"]

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)

        category_serializer = CategorySerializer(instance=instance.category)
        representation["category"] = category_serializer.data

        tag_serializer = TagSerializer(instance=instance.tags, many=True)
        representation["tags"] = tag_serializer.data

        representation["image"] = instance.image.name.split("/")[-1]

        return representation

    def validate_user(self, user):
        if user is None:
            raise serializers.ValidationError(detail="User is required.")

        return user

    def validate_title(self, title):
        if title == "":
            raise serializers.ValidationError(detail="Title is required.")

        if title and len(title) < 10:
            raise serializers.ValidationError(
                detail="The title must be at least 10 characters long."
            )

        if title and len(title) >= 10 and Article.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                detail="The given article title already exists."
            )

        return title

    def validate_content(self, content):
        if content == "":
            raise serializers.ValidationError(
                detail="Content is required."
            )

        if content and len(content) < 10:
            raise serializers.ValidationError(
                detail="The content must be at least 10 characters long."
            )

        return content

    def validate_image(self, image):
        if image is None:
            raise serializers.ValidationError(detail="Image is required.")

        extension = image.name.split(".")[-1]
        allowed_extensions = ["jpg", "jpeg", "png", "svg", "webp"]

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                detail="Invalid file format. Allowed formats are 'jpg', 'jpeg', 'png', 'svg', 'webp'."
            )

        return image

    def validate_category(self, category):
        if category is None:
            raise serializers.ValidationError(detail="Category is required.")

        return category

    def validate_tags(self, tags):
        if len(tags) == 0:
            raise serializers.ValidationError(
                detail="You must select at least one tag."
            )

        return tags


class ArticleUpdateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text="Select the article author.",
        required=False,
        allow_null=True,
    )
    title = serializers.CharField(max_length=1000, help_text="Enter the article title.", required=False,
                                  allow_blank=True)
    content = serializers.CharField(max_length=100000, help_text="Enter the article content.", required=False,
                                    allow_blank=True)
    image = serializers.ImageField(help_text="Upload the main article image.", required=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        help_text="Select the article category.",
        required=False,
        allow_null=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        help_text="Select at least one tag.",
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Article
        fields = [
            "id",
            "user",
            "title",
            "content",
            "image",
            "category",
            "tags",
            "slug",
        ]
        read_only_fields = ["id", "slug"]

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)
        representation["image"] = instance.image.name.split("/")[-1]

        return representation

    def validate_user(self, user):
        if user is None:
            raise serializers.ValidationError(detail="User is required.")

        return user

    def validate_title(self, title):
        if title == "":
            raise serializers.ValidationError(detail="Title is required")

        if title and len(title) < 10:
            raise serializers.ValidationError(detail="The title must be at least 10 characters long.")

        if self.instance.title != title and Article.objects.filter(title=title).exists():
            raise serializers.ValidationError(detail="An article with this title already exists.")

        return title

    def validate_content(self, content):
        if content == "":
            raise serializers.ValidationError(detail="Content is required.")

        if content and len(content) < 10:
            raise serializers.ValidationError(
                detail="The content must be at least 10 characters long."
            )

        return content

    def validate_image(self, image):
        extension = image.name.split(".")[-1]
        allowed_extensions = ["jpg", "jpeg", "png", "svg", "webp"]

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                detail="Invalid file format. Allowed formats are 'jpg', 'jpeg', 'png', 'svg', 'webp'."
            )

        return image

    def validate_category(self, category):
        if category is None:
            raise serializers.ValidationError(detail="Category is required.")

        return category

    def validate_tags(self, tags):
        if len(tags) == 0:
            raise serializers.ValidationError(detail="You must select at least one tag.")

        return tags


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "date_posted",
            "user",
            "full_name",
            "article",
            "comment",
            "active",
            "likes",
            "dislikes",
            "lft",
            "rght",
            "tree_id",
            "level",
            "parent",
        ]
        extra_kwargs = {
            "date_posted": {
                "format": "%Y-%m-%d %H:%M:%S",
                "read_only": True,
            }
        }


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "user",
            "full_name",
            "article",
            "comment",
            "level",
            "parent",
        ]
