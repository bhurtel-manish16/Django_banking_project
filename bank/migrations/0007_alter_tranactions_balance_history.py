# Generated by Django 4.1.7 on 2023-03-18 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bank", "0006_tranactions_balance_history"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tranactions",
            name="balance_history",
            field=models.CharField(max_length=14),
        ),
    ]
