# Generated by Django 4.2.7 on 2024-01-02 19:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_user_uuid_alter_onetimepassword_expires_in_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="uuid",
        ),
        migrations.AlterField(
            model_name="business",
            name="company_id",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="business",
            name="company_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="business",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="individual",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_in",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 1, 2, 19, 47, 47, 677181, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
