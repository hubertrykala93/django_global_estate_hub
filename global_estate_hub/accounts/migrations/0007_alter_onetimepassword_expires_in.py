# Generated by Django 4.2.7 on 2024-01-01 23:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_onetimepassword_expires_in"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_in",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 1, 1, 23, 21, 23, 484835, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
