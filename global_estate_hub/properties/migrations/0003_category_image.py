# Generated by Django 4.2.7 on 2024-01-26 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0002_property_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="image",
            field=models.ImageField(null=True, upload_to=""),
        ),
    ]
