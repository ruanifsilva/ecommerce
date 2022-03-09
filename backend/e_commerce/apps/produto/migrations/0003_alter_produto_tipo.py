# Generated by Django 4.0.1 on 2022-03-07 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("produto", "0002_variacao"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produto",
            name="tipo",
            field=models.CharField(
                choices=[("V", "Variável"), ("S", "Simples")], default="V", max_length=1
            ),
        ),
    ]
