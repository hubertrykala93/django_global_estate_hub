# Generated by Django 4.2.7 on 2023-11-10 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0011_alter_user_otp_expire"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="otp_expire",),
        migrations.RemoveField(model_name="user", name="otp_send",),
    ]
