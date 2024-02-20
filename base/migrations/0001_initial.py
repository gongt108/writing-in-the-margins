# Generated by Django 5.0.2 on 2024-02-20 09:21

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("book_cover", models.CharField()),
                ("title", models.CharField()),
                ("contributors", models.CharField()),
                ("avg_rating", models.CharField()),
                ("num_rating", models.CharField()),
                ("description", models.TextField()),
                ("genres", models.CharField()),
                ("page_num", models.CharField()),
                ("publication_date", models.CharField()),
                ("book_id", models.CharField()),
            ],
        ),
    ]