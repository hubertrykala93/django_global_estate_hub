# Generated by Django 4.2.7 on 2024-01-22 12:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0063_alter_onetimepassword_expires_in"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_in",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 1, 22, 12, 49, 53, 599093, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
