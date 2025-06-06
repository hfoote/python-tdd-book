# Generated by Django 5.1.4 on 2025-05-22 20:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lists", "0004_item_list"),
    ]

    operations = [
        migrations.AlterModelOptions(name="item", options={"ordering": ["id"]},),
        migrations.AlterField(
            model_name="item",
            name="list",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="lists.list",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="item", unique_together={("list", "text")},
        ),
    ]
