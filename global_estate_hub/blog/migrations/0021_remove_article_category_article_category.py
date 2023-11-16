# Generated by Django 4.2.7 on 2023-11-16 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0020_remove_article_category_article_category"),
    ]

    operations = [
        migrations.RemoveField(model_name="article", name="category",),
        migrations.AddField(
            model_name="article",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="article",
                to="blog.category",
            ),
        ),
    ]
