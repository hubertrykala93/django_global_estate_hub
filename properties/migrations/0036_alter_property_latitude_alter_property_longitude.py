# Generated by Django 4.2.7 on 2024-06-28 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0035_alter_property_city"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="latitude",
            field=models.FloatField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="property",
            name="longitude",
            field=models.FloatField(blank=True, max_length=20, null=True),
        ),
    ]
