# Generated by Django 4.1.3 on 2023-03-13 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bank", "0002_payment_username"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tranactions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField()),
                ("description", models.CharField(max_length=100)),
                ("amount", models.CharField(max_length=100000000000000000000)),
            ],
        ),
    ]