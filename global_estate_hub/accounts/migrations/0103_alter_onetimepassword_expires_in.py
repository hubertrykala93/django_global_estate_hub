# Generated by Django 4.2.7 on 2023-12-17 10:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0102_alter_onetimepassword_expires_in"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_in",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 12, 17, 10, 23, 4, 989699, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
