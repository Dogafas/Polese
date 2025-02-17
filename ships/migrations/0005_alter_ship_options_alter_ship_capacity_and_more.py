# Generated by Django 5.1.6 on 2025-02-14 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ships", "0004_alter_ship_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ship",
            options={
                "verbose_name": "Судно",
                "verbose_name_plural": "Суда (теплоходы)",
            },
        ),
        migrations.AlterField(
            model_name="ship",
            name="capacity",
            field=models.IntegerField(verbose_name="Вместимость"),
        ),
        migrations.AlterField(
            model_name="ship",
            name="description",
            field=models.TextField(verbose_name="Описание"),
        ),
        migrations.AlterField(
            model_name="ship",
            name="name",
            field=models.CharField(max_length=255, verbose_name="Название судна"),
        ),
        migrations.AlterField(
            model_name="ship",
            name="ship_id",
            field=models.AutoField(
                primary_key=True, serialize=False, verbose_name="ID судна"
            ),
        ),
    ]
