from tkinter.font import names

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:user_id>/attending/", views.attending, name="attending"),
    path("<int:user_id>/home/", views.user_home, name="user_home"),
    path("<int:user_id>/attending/<int:party_id>", views.party, name="party"),
    path("<int:user_id>/hosting/", views.hosting, name="hosting"),
    path("<int:user_id>/dashboard/<int:party_id>", views.dashboard, name="dashboard"),
]