# Generated by Django 4.2.7 on 2024-03-28 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0031_alter_img_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="img",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="property_details_images"
            ),
        ),
    ]
