# Generated by Django 4.2.7 on 2024-01-11 20:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0041_alter_onetimepassword_expires_in"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_in",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 1, 11, 20, 14, 58, 52050, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
