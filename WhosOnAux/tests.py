from django.test import TestCase
from django.test import Client
# from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from WhosOnAux.models import Party, Playlist, Attending
from .forms import NewPartyForm, InviteGuestForm

import WhosOnAux.views
from WhosOnAux.spotify_utils import SpotifyPlaylist
# Create your tests here.

REDIRECT_302 = 302   # "Found" or "Moved Temporarily" |Temporarily relocate a site to a new URL
OK_200 = 200         # GET A resource was retrieved and included in the response body
ERROR404 = 404

client = Client()
# request = HttpRequest
class URLsTests(TestCase):
    def test_landing_url(self):
        response = client.get("")
        self.assertEqual(response.status_code, 200)

    def test_user_home_url_authenticated(self):
        user = User.objects.create(username="Testuser")
        client.force_login(user)
        response = client.get(f"/home/")
        self.assertEqual(response.status_code, OK_200)

    def test_user_home_url_not_authenticated(self):
        response = self.client.get(f"/home/")
        self.assertEqual(response.status_code, REDIRECT_302)

    def test_user_hosting_url_not_authenticated(self):
        response = client.get(f"/hosting/")
        self.assertEqual(response.status_code, REDIRECT_302)

    def test_user_hosting_url_authenticated(self):
        user = User.objects.create(username="Testuser")
        client.force_login(user)
        response = client.get(f"/hosting/")
        self.assertEqual(response.status_code, OK_200)

    def test_create_new_party_url(self):
        user = User.objects.create(username="Testuser")
        self.client.force_login(user)
        form_data = {"party_name": "A party name",
                     "description": "short description of party"}
        response = self.client.post(reverse("create_new_party"), form_data)
        self.assertEqual(response.status_code, 302)

    def test_create_new_party_invalid(self):
        user = User.objects.create(username="Testuser")
        self.client.force_login(user)
        form_data = {}   # invalid entry
        response = self.client.post(reverse("create_new_party"), form_data)
        self.assertEqual(response.status_code, ERROR404)

    def test_user_attending_url_not_authenticated(self):
        response = client.get(f"/attending/")
        self.assertEqual(response.status_code, REDIRECT_302)

    def test_user_attending_url_authenticated(self):
        user = User.objects.create(username="Testuser")
        host = User.objects.create(username="host")
        party_invited = Party.objects.create(name="invited", host=host)
        party_uninvited = Party.objects.create(name="uninvited", host=host)
        Attending.objects.create(party=party_invited, attendee=user)
        client.force_login(user)
        response = client.get(f"/attending/")
        self.assertEqual(response.status_code, OK_200)
        self.assertIn(party_invited, response.context["attending_parties"])
        self.assertNotIn(party_uninvited, response.context["attending_parties"])

    def test_attending_party_url(self):
        user = User.objects.create(username="Testuser")
        party = Party.objects.create(host=user, name="TestParty")
        response = client.get(f"/attending/{party.id}")
        self.assertEqual(response.status_code, 200)

    def test_party_dashboard_url_not_authenticated(self):
        """
        user is not authenticated
        :return:
        """
        user = User.objects.create(username="Testuser")
        party = Party.objects.create(host=user, name="TestParty")
        response = client.get(f"/dashboard/{party.id}")
        self.assertEqual(response.status_code, REDIRECT_302)

    def test_party_dashboard_url_authenticated_host(self):
        """
        user is authenticated
        :return:
        """
        user = User.objects.create(username="Testuser")
        client.force_login(user)
        party = Party.objects.create(host=user, name="TestParty")
        response = client.get(f"/dashboard/{party.id}")
        self.assertEqual(response.status_code, OK_200)

    def test_party_dashboard_url_user_not_host(self):
        """
        User is authenticated, but is not the host of the party
        redirect to attendee view of party
        :return:
        """
        host = User.objects.create(username="Host")
        attendee = User.objects.create(username="Attendee")
        party = Party.objects.create(host=host, name="TestParty")
        client.force_login(attendee)
        response = client.get(f"/dashboard/{party.id}")
        self.assertEqual(response.status_code, REDIRECT_302)

    def test_invite_guest_url(self):
        host = User.objects.create(username="Testuser")
        self.client.force_login(host)
        form_data = {'email':"guest@example.com"}
        response = self.client.post(reverse("invite_guest"), form_data)
        self.assertEqual(response.status_code, 302)

    def test_invite_guest_invalid(self):
        host = User.objects.create(username="Testuser")
        self.client.force_login(host)
        form_data = {}   # invalid entry
        response = self.client.post(reverse("invite_guest"), form_data)
        self.assertEqual(response.status_code, ERROR404)

class NewPartyFormTests(TestCase):
    def test_valid_form(self):
        name = "A party name"
        description = "short description of party"
        form_data = {"party_name": name, "description": description}
        form = NewPartyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_no_data(self):
        form = NewPartyForm()
        self.assertFalse(form.is_valid())

class InviteGuestFormTests(TestCase):
    def setUp(self):
        self.host = User.objects.create_user(username='Host')
        self.client = Client()
        client.force_login(self.host)
    def test_valid_form(self):
        form_data = {'email':'guest@example.com'}
        form = InviteGuestForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invite_sent(self):
        form_data = {'email': 'guest@example.com'}
        response = self.client.post(reverse('invite_guest'), form_data)
        self.assertEqual(len(mail.outbox), 1)  # 1 email should have been sent
        self.assertIn('guest@example.com', mail.outbox[0].to)

class ModelsTests(TestCase):
    def test_party_get_name(self):
        user = User.objects.create(username="Testuser")
        party = Party(host=user, name="TestParty")
        self.assertTrue(party.name == "TestParty")

    def test_party_get_str(self):
        user = User.objects.create(username="Testuser")
        party = Party(host=user, name="TestParty")
        self.assertTrue(str(party) == "TestParty")

    def test_playlist_get_name(self):
        user = User.objects.create(username="Testuser")
        song = Playlist(name="TestPlaylist", added_by=user)
        self.assertTrue(song.name == "TestPlaylist")

    def test_playlist_get_str(self):
        user = User.objects.create(username="Testuser")
        song = Playlist(name="TestPlaylist", added_by=user)
        self.assertTrue(str(song) == "TestPlaylist")

# class SpotifyUtilsTests(TestCase):
#     # TODO: authentication fails in github actions
#     # comment out for push
#     def setUp(self):
#         example_url = '3cEYpjA9oz9GiPac4AsH4n'
#         self.test_playlist = SpotifyPlaylist(example_url)
#
#     def test_get_image(self):
#         actual_url = 'https://image-cdn-ak.spotifycdn.com/image/ab67706c0000bebb8d0ce13d55f634e290f744ba'
#         json_data = self.test_playlist.get_image_details()[0]
#         test_url = json_data['url']
#         self.assertEqual(test_url, actual_url)
#
#     def test_get_tracks(self):
#         actual_id = '4rzfv0JLZfVhOhbSQ8o5jZ'
#         items = self.test_playlist.get_tracks()
#         test_id = items[0]['track']['id']
#         self.assertEqual(test_id, actual_id)

# TODO: Login tests
