# Generated by Django 4.2.7 on 2024-04-24 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0034_alter_city_image_alter_city_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="city",
            field=models.ForeignKey(
                blank=True,
                default="",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cities",
                to="properties.city",
            ),
        ),
    ]