# Generated by Django 4.2.2 on 2023-06-09 17:34

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MarketClosingData",
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
                ("date", models.DateField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("volume", models.DecimalField(decimal_places=1, max_digits=10)),
            ],
        ),
    ]
