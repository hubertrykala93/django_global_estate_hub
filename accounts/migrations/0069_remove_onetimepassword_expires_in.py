# Generated by Django 4.2.7 on 2024-03-19 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0068_onetimepassword_expires_in_alter_user_is_agent"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="onetimepassword",
            name="expires_in",
        ),
    ]
