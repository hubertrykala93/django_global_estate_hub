# Generated by Django 4.2.7 on 2024-01-03 13:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0017_alter_onetimepassword_expires_in"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_in",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 1, 3, 13, 32, 54, 628526, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
