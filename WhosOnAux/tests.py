from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from WhosOnAux.models import Party, Playlist, Attending
from .forms import NewPartyForm, InviteGuestForm

import WhosOnAux.spotify_utils as spotify_utils
from unittest.mock import MagicMock

# Create your tests here.

REDIRECT_302 = 302   # "Found" or "Moved Temporarily" |Temporarily relocate a site to a new URL
OK_200 = 200         # GET A resource was retrieved and included in the response body
ERROR404 = 404

client = Client()

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
        host = User.objects.create(username="Host")
        guest = User.objects.create(username="Guest")
        client.force_login(guest)
        party = Party.objects.create(host=host, name="TestParty")
        Attending.objects.create(party=party, attendee=guest)
        response = client.get(f"/attending/{party.id}")
        self.assertEqual(response.status_code, OK_200)

    def test_attending_party_url_host(self):
        host = User.objects.create(username="Host")
        party = Party.objects.create(host=host, name="TestParty")
        client.force_login(host)
        response = client.get(f"/attending/{party.id}")
        self.assertEqual(response.status_code, REDIRECT_302)

    def test_attending_party_url_not_invited(self):
        host = User.objects.create(username="Host")
        party = Party.objects.create(host=host, name="TestParty")
        uninvited = User.objects.create(username="Uninvited")
        client.force_login(uninvited)
        response = client.get(f"/attending/{party.id}")
        self.assertEqual(response.status_code, REDIRECT_302)

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

class SpotifyUtilsTests(TestCase):
    def setUp(self):
        """
        MagicMock calls to spotify API and create a playlist for testing
        :return:
        """
        # example_url = '3cEYpjA9oz9GiPac4AsH4n'
        fake_url = 'fakeurl'
        spotify_utils.get_token = MagicMock(return_value='fake_token')
        spotify_utils.SpotifyPlaylist.get_image_details = MagicMock(return_value=[{'url':'fake_image_url'}])
        spotify_utils.SpotifyPlaylist.get_tracks = MagicMock(return_value={'tracks_keys':'tracks_values'})
        self.test_playlist = spotify_utils.SpotifyPlaylist(fake_url)

    def test_SpotifyPlaylist_token(self):
        token = self.test_playlist.token
        self.assertEqual(token, 'fake_token')

    def test_SpotifyPlaylist_auth_header(self):
        token = spotify_utils.get_token()
        test_auth_header = self.test_playlist.auth_header
        actual_auth_header = {"Authorization": "Bearer " + token}
        self.assertEqual(test_auth_header, actual_auth_header)

    def test_get_image(self):
        # actual_url = 'https://image-cdn-fa.spotifycdn.com/image/ab67706c0000bebb8d0ce13d55f634e290f744ba'
        actual_url = 'fake_image_url'  # MagicMaocked
        json_data = self.test_playlist.get_image_details()[0]
        test_url = json_data['url']
        self.assertEqual(test_url, actual_url)

    def test_get_tracks(self):
        actual_tracks = {'tracks_keys':'tracks_values'}   #MagicMocked
        test_tracks = self.test_playlist.get_tracks()
        self.assertEqual(test_tracks, actual_tracks)


# TODO: Login tests
