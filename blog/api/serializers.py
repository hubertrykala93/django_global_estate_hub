from blog.models import Category, Tag, Article, Comment
from accounts.models import User
from rest_framework import serializers


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ArticleTagsSerializer(serializers.ModelSerializer):
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
        allow_null=True,
    )
    title = serializers.CharField(max_length=1000, allow_blank=True)
    content = serializers.CharField(max_length=100000, allow_blank=True)
    image = serializers.ImageField(allow_null=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
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

        category_serializer = ArticleCategorySerializer(instance=instance.category)
        representation["category"] = category_serializer.data

        tag_serializer = ArticleTagsSerializer(instance=instance.tags, many=True)
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
            raise serializers.ValidationError(detail="Content is required.")

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
        allow_null=True,
        required=False,
    )
    title = serializers.CharField(max_length=1000, allow_blank=True, required=False)
    content = serializers.CharField(max_length=100000, allow_blank=True, required=False)
    image = serializers.ImageField(required=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True, required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
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
            raise serializers.ValidationError(
                detail="The title must be at least 10 characters long."
            )

        if (
            self.instance.title != title
            and Article.objects.filter(title=title).exists()
        ):
            raise serializers.ValidationError(
                detail="An article with this title already exists."
            )

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
            raise serializers.ValidationError(
                detail="You must select at least one tag."
            )

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
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.none(),
        help_text="Select the comment author. If the comment author is selected, skip the 'Full Name' field.",
        required=False,
        allow_null=True,
    )
    full_name = serializers.CharField(
        label="Full Name",
        required=False,
        help_text="Fill in only if you are not using the User field. The comment will be added by an anonymous user.",
        allow_blank=True,
    )
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all(),
        help_text="Select the article to which you want to assign your comment. Your comment will be the main comment. "
        "If you want to assign a comment to a comment, skip this field and use the 'Parent' field.",
        required=True,
    )
    comment = serializers.CharField(
        max_length=10000,
        help_text="Enter the comment content.",
        allow_blank=True,
        required=True,
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        help_text="Select the comment to which you want to assign your comment using the 'Parent' field. "
        "Skip the 'Article' field.",
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "full_name",
            "article",
            "comment",
            "parent",
            "active",
        ]
        extra_kwargs = {
            "active": {
                "read_only": True,
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.context.get("request").user

        if user.is_staff:
            self.fields["user"].queryset = User.objects.all()
            self.fields["user"].allow_null = True

        else:
            self.fields["user"].queryset = User.objects.filter(username=user)
            self.fields["user"].allow_null = False
            self.fields.pop("full_name", None)

    def validate_user(self, user):
        if user is not None:
            if self.context.get("full_name"):
                raise serializers.ValidationError(
                    detail="You cannot provide both 'User' and 'Full Name'. "
                    "If you want to create a comment for an authenticated user, "
                    "fill in only the 'User' field and leave the 'Full Name' field empty."
                )

        if user is None and self.context.get("full_name") is None:
            raise serializers.ValidationError(
                detail="You must provide one of the fields: 'User' or 'Full Name'. "
                "If you want to create a comment for a logged-in user, select the 'User' field. "
                "If you want to create a comment for an anonymous user, select the 'Full Name' field."
            )

        return user

    def validate_full_name(self, full_name):
        if self.context.get("full_name"):
            if self.context.get("user"):
                raise serializers.ValidationError(
                    detail="You cannot provide both 'Full Name' and 'User'. "
                    "If you want to create a comment for an anonymous user, "
                    "fill in only the 'Full Name' field and leave the 'User' field empty."
                )

        return full_name

    def validate_article(self, article):
        if self.context.get("parent"):
            if (
                Comment.objects.get(id=int(self.context.get("parent"))).article
                != article
            ):
                raise serializers.ValidationError(
                    detail=f"Incorrect 'Parent' for this article. "
                    f"You can only add a reply to a comment associated with the article {article}. "
                    f"The list of comment IDs associated with the article {article} is {[comment.id for comment in article.comments.all()]}."
                )

        return article

    def validate_parent(self, parent):
        if parent and parent.article.id != int(self.context.get("article_id")):
            raise serializers.ValidationError(
                detail=f"The selected parent comment does not belong to the chosen article. "
                f"The parent comment is associated with the article {Article.objects.get(id=parent.article.id).title}."
            )

        return parent

    def validate_comment(self, comment):
        if comment == "":
            raise serializers.ValidationError(detail="Comment is required.")

        if comment and len(comment) < 10:
            raise serializers.ValidationError(
                detail="The comment should be at least 10 characters long."
            )

        return comment

    def create(self, validated_data):
        if self.context.get("request"):
            if self.context.get("request").user.is_staff:
                validated_data["active"] = True

            else:
                validated_data["active"] = False

        return super().create(validated_data=validated_data)


class CommentUpdateSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(
        max_length=10000,
        help_text="Update the content of the comment.",
        allow_blank=True,
        required=False,
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "comment",
        ]

    def validate_comment(self, comment):
        if comment == "":
            raise serializers.ValidationError(detail="Comment is required.")

        return comment
