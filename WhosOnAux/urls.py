from tkinter.font import names

from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("attending/", views.attending, name="attending"),
    # ex: /001/attending/
    path("home/", views.user_home, name="user_home"),
    # ex: home/
    path("attending/<int:party_id>", views.party, name="party"),
    # ex: /001/attending/001
    path("hosting/", views.hosting, name="hosting"),
    # ex: /001/hosting/
    path("<int:user_id>/dashboard/<int:party_id>", views.dashboard, name="dashboard"),
    # ex: /001/dashboard/001
]
