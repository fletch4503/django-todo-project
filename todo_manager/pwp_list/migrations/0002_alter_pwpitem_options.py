# Generated by Django 5.1.1 on 2024-09-10 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pwp_list", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="pwpitem",
            options={"ordering": ("id",), "verbose_name": "PWP Item"},
        ),
    ]
