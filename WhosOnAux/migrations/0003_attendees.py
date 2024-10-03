# Generated by Django 5.1 on 2024-10-03 17:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("WhosOnAux", "0002_delete_attendees"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendees",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NR", "No response"),
                            ("Y", "Yes"),
                            ("N", "No"),
                            ("M", "Maybe"),
                        ],
                        max_length=3,
                    ),
                ),
                (
                    "attendee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "party_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="WhosOnAux.party",
                    ),
                ),
            ],
        ),
    ]
