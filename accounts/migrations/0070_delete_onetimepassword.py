# Generated by Django 4.2.7 on 2024-03-24 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0069_remove_onetimepassword_expires_in"),
    ]

    operations = [
        migrations.DeleteModel(
            name="OneTimePassword",
        ),
    ]
