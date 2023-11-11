# Generated by Django 4.2.7 on 2023-11-11 07:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0021_remove_user_one_time_password_created_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="onetimepassword", name="sent",),
        migrations.AddField(
            model_name="onetimepassword",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 11, 11, 7, 15, 13, 67653, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AddField(
            model_name="onetimepassword",
            name="is_sent",
            field=models.BooleanField(default=False),
        ),
    ]
