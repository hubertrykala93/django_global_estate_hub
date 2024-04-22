# Generated by Django 4.2.7 on 2024-03-05 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0007_alter_property_purchasing_user_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="property",
            name="image_files",
        ),
        migrations.RemoveField(
            model_name="property",
            name="main_image",
        ),
        migrations.AddField(
            model_name="property",
            name="images",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="property_images/<django.db.models.fields.CharField>",
            ),
        ),
    ]
