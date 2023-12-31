# Generated by Django 4.2.3 on 2023-07-22 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Edition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("current", models.BooleanField(default=False, verbose_name="Set this as the current Edition")),
            ],
        ),
        migrations.CreateModel(
            name="ItemGroup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "scheme",
                    models.CharField(
                        choices=[("AS", "ASA Relative Value Guide"), ("MB", "Medicare Benefits Scheme")],
                        default="AS",
                        max_length=2,
                    ),
                ),
                ("description", models.CharField(max_length=255)),
                ("code", models.CharField(max_length=20)),
                ("units", models.IntegerField(blank=True, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="bills.category"
                    ),
                ),
                (
                    "edition",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="bills.edition"
                    ),
                ),
                (
                    "item_group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="bills.itemgroup",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Case",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateTimeField(default=django.utils.timezone.now, verbose_name="Procedure date")),
                ("initials", models.CharField(max_length=10, verbose_name="Patient initials")),
                ("dob", models.DateField(verbose_name="Patient date of birth")),
                ("procedure", models.CharField(max_length=255, verbose_name="Procedure details")),
                (
                    "processed",
                    models.DateTimeField(blank=True, null=True, verbose_name="The date this bill was processed"),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("items", models.ManyToManyField(to="bills.item")),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="bills.profile")),
            ],
        ),
    ]
