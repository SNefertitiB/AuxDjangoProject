# Generated by Django 5.1 on 2024-10-03 17:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("WhosOnAux", "0006_rename_party_id_attendees_party"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendees",
            name="status",
            field=models.CharField(
                choices=[
                    ("NR", "No response"),
                    ("Y", "Yes"),
                    ("N", "No"),
                    ("M", "Maybe"),
                ],
                default="NR",
                max_length=12,
            ),
        ),
    ]
