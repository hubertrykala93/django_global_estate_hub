# Generated by Django 4.2.7 on 2024-03-25 22:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0070_delete_onetimepassword"),
    ]

    operations = [
        migrations.AlterField(
            model_name="individual",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
