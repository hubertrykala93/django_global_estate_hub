# Generated by Django 4.2.7 on 2024-01-01 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="slug",
            field=models.SlugField(max_length=300, null=True, unique=True),
        ),
    ]
