# Generated by Django 4.2.7 on 2023-11-29 12:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0088_alter_onetimepassword_expires_in"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user", old_name="is_company", new_name="is_business",
        ),
        migrations.RenameField(
            model_name="user", old_name="is_private", new_name="is_individual",
        ),
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_in",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 11, 29, 12, 41, 32, 457987, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]