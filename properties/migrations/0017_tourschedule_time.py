# Generated by Django 4.2.7 on 2024-03-17 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0016_rename_to_tourschedule_customer"),
    ]

    operations = [
        migrations.AddField(
            model_name="tourschedule",
            name="time",
            field=models.CharField(max_length=100, null=True),
        ),
    ]