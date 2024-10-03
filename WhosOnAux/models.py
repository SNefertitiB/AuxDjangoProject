import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
# class ClassName(models.Model):
#    class_name_text = models.FieldType(kwargs=value)
#    see: https://docs.djangoproject.com/en/5.1/ref/models/fields/#field-types


# class Profile(models.Model):
#     pass
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # user_ID = models.AutoField(primary_key=True)


class Party(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    party_id = models.AutoField(primary_key=True)
    playlist_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    # date = models.DateTimeField("event date")  # TODO: error message, needs default value
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Playlist(models.Model):
    """
    TODO: not sure this is the most efficient way to store the playlist
    This will store all playlist transactions in one database
    might be better to create a new database for each party?
    database can then be destroyed 1 week after party date?
    """
    name = models.CharField(max_length=200)       # spotify_id
    track_name = models.CharField(max_length=200)
    track_ID = models.CharField(max_length=200)    # spotify_id
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)    # User
    # added_date = models.DateTimeField("added date") # TODO: error message, needs default value

    def __str__(self):
        return self.name


# class Attendees(models.Model):
#     party = models.ForeignKey(Party, on_delete=models.CASCADE)        # Party
#     attendee = models.ForeignKey(User, on_delete=models.CASCADE)      # User
#     NO_RESPONSE = "NR"
#     YES = "Y"
#     NO = "N"
#     MAYBE = "M"
#     STATUS_CHOICES = {
#                 NO_RESPONSE: "No response",
#                 YES: "Yes",
#                 NO: "No",
#                 MAYBE: "Maybe"
#     }
#     status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=NO_RESPONSE)

