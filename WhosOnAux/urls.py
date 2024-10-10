from tkinter.font import names

from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("attending/", views.attending, name="attending"),
    # ex: /attending/
    path("home/", views.user_home, name="user_home"),
    # ex: /home/
    path("attending/<int:party_id>", views.party, name="party"),
    # ex: /attending/001
    path("hosting/", views.hosting, name="hosting"),
    # ex: /hosting/
    path("create_new_party/", views.create_new_party, name="create_new_party"),
    # ex: /create_new_party/
    path("dashboard/<int:party_id>", views.dashboard, name="dashboard"),
    # ex: /dashboard/001
]
