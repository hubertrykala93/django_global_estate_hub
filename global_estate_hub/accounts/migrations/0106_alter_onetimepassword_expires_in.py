# Generated by Django 4.2.7 on 2023-12-17 14:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0105_alter_onetimepassword_expires_in_alter_user_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_in",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 12, 17, 14, 20, 43, 931119, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
