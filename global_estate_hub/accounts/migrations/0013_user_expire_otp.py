# Generated by Django 4.2.7 on 2023-11-10 20:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_remove_user_otp_expire_remove_user_otp_send"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="expire_otp",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 11, 10, 20, 51, 51, 371767, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
