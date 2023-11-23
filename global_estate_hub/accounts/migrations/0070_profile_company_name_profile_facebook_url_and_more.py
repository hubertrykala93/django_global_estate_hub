# Generated by Django 4.2.7 on 2023-11-22 21:56

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0069_alter_onetimepassword_expires_in"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="company_name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profile", name="facebook_url", field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="instagram_url",
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name="profile", name="linkedin_url", field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="phone_number",
            field=models.CharField(max_length=31, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="postal_code",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="street",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profile", name="website_url", field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name="onetimepassword",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_in",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 11, 22, 22, 1, 0, 244905, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="city",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="country",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="first_name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="last_name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="province",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user", name="last_login", field=models.DateTimeField(null=True),
        ),
    ]
