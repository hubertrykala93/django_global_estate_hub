# Generated by Django 4.2.7 on 2023-11-10 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0017_alter_user_otp_expire"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="one_time_password_sent_email",
            field=models.BooleanField(default=False),
        ),
    ]
