# Generated by Django 4.2.7 on 2024-03-05 12:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0012_amenities_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tourschedule",
            old_name="email",
            new_name="phone_number",
        ),
        migrations.RemoveField(
            model_name="review",
            name="full_name",
        ),
        migrations.AlterField(
            model_name="amenities",
            name="image",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="icons/properties",
                validators=[django.core.validators.FileExtensionValidator(["svg"])],
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="active",
            field=models.BooleanField(default=True),
        ),
    ]
