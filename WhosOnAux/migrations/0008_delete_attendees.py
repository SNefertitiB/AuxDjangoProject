# Generated by Django 5.1 on 2024-10-03 17:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("WhosOnAux", "0007_alter_attendees_status"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Attendees",
        ),
    ]
