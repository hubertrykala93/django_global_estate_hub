# Generated by Django 4.2.7 on 2023-11-13 16:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0047_alter_onetimepassword_expires_in"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_in",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 11, 13, 17, 0, 22, 207245, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
