# Generated by Django 4.2.7 on 2024-02-21 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("properties", "0005_city_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="purchasing_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="quantity_of_purchases",
            field=models.IntegerField(default=0, null=True),
        ),
    ]
