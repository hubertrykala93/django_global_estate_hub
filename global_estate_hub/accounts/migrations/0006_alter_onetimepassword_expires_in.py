# Generated by Django 4.2.7 on 2024-01-01 22:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_onetimepassword_expires_in_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_in",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 1, 1, 22, 57, 45, 998139, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
