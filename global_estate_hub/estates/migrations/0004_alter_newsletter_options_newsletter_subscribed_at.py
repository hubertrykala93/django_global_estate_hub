# Generated by Django 4.2.6 on 2023-11-03 09:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("estates", "0003_alter_newsletter_email"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="newsletter",
            options={
                "ordering": ["-subscribed_at"],
                "verbose_name_plural": "Newsletters",
            },
        ),
        migrations.AddField(
            model_name="newsletter",
            name="subscribed_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
