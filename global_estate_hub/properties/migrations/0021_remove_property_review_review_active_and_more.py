# Generated by Django 4.2.7 on 2024-01-08 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0020_offercontact_date_sent"),
    ]

    operations = [
        migrations.RemoveField(model_name="property", name="review",),
        migrations.AddField(
            model_name="review",
            name="active",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="review",
            name="date_sent",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="review",
            name="property",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="properties.property",
            ),
        ),
    ]
