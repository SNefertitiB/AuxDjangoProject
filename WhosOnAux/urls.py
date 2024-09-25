from tkinter.font import names

from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("<int:user_id>/attending/", views.attending, name="attending"),
    # ex: /001/attending/
    path("<int:user_id>/home/", views.user_home, name="user_home"),
    # ex: /001/home/
    path("<int:user_id>/attending/<int:party_id>", views.party, name="party"),
    # ex: /001/attending/001/
    path("<int:user_id>/hosting", views.hosting, name="hosting"),
    # ex: /001/hosting
    path("<int:user_id>/dashboard/<int:party_id>", views.dashboard, name="dashboard"),
    # ex: /001/dashboard/001
]
