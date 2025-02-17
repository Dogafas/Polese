# Generated by Django 5.1.6 on 2025-02-14 12:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("routes", "0007_alter_routepoint_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="stop",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Дата создания",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="stop",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
        ),
    ]
