from django.contrib import admin

from .models import Question, Party, Playlist

# Register your models here.
admin.site.register(Question)
admin.site.register(Party)
admin.site.register(Playlist)
