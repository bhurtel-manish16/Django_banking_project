# Generated by Django 4.1.7 on 2023-03-18 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bank", "0005_tranactions_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="tranactions",
            name="balance_history",
            field=models.CharField(default="", max_length=14),
        ),
    ]
