# Generated by Django 4.2 on 2023-04-21 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_login",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last login"
            ),
        ),
        migrations.AlterField(
            model_name="user", name="email", field=models.EmailField(max_length=40),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
