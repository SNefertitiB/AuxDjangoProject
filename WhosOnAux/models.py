import datetime

from django.db import models
from django.utils import timezone
# Create your models here.
# class ClassName(models.Model):
#    class_name_text = models.FieldType(kwargs=value)
#    see: https://docs.djangoproject.com/en/5.1/ref/models/fields/#field-types


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Party(models.Model):
    host_id = models.IntegerField(default=0)
    party_id = models.IntegerField(default=0)
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
    added_by = models.IntegerField(default=0)      # user_id
    # added_date = models.DateTimeField("added date") # TODO: error message, needs default value
    def __str__(self):
        return self.name


class Attendees(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)   # party_id
    attendee = models.IntegerField()                                # user_id


