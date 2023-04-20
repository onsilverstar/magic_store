# Generated by Django 4.2 on 2023-04-20 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
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
                ("address", models.CharField(max_length=20)),
                ("zip_code", models.CharField(max_length=20)),
                ("state", models.CharField(max_length=20)),
                ("city", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("item_number", models.IntegerField()),
                ("cost", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("product_name", models.CharField(max_length=20)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "guid",
                    models.CharField(max_length=40, primary_key=True, serialize=False),
                ),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                ("rating", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                ("email", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=20)),
                (
                    "address",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="store.address"
                    ),
                ),
                (
                    "order_items",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.orderitem",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="orderitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="store.product"
            ),
        ),
        migrations.CreateModel(
            name="Order",
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
                ("order_total", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "items",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.orderitem",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Categories",
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
                ("category_name", models.CharField(max_length=20)),
                (
                    "products",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.product"
                    ),
                ),
            ],
        ),
    ]