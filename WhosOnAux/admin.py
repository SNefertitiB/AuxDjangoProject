from django.contrib import admin

from .models import Profile, Party, Playlist

# Register your models here.
admin.site.register(Profile)
admin.site.register(Party)
admin.site.register(Playlist)
