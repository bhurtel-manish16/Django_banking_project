# Generated by Django 4.1.1 on 2023-01-27 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bank", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="username",
            field=models.CharField(default="john", max_length=20),
            preserve_default=False,
        ),
    ]