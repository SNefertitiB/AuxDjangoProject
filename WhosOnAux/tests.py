from django.test import TestCase
from django.test import Client
from django.http import HttpRequest
from django.contrib.auth.models import User
from WhosOnAux.models import Party

import WhosOnAux.views
# Create your tests here.

client = Client()
# request = HttpRequest
class URLsTests(TestCase):
    def test_landing_url(self):
        response = client.get("")
        self.assertEqual(response.status_code, 200)

    def test_user_home_url(self):
        user = User.objects.create(username="Testuser")
        response = client.get(f"/{user.id}/home/")
        self.assertEqual(response.status_code, 200)

    def test_user_hosting_url(self):
        user = User.objects.create(username="Testuser")
        response = client.get(f"/{user.id}/hosting/")
        self.assertEqual(response.status_code, 200)

    def test_user_attending_url(self):
        user = User.objects.create(username="Testuser")
        response = client.get(f"/{user.id}/attending/")
        self.assertEqual(response.status_code, 200)

    def test_attending_party_url(self):
        user = User.objects.create(username="Testuser")
        party = Party.objects.create(host=user, name="TestParty")
        response = client.get(f"/{user.id}/attending/{party.party_id}")
        self.assertEqual(response.status_code, 200)

    def test_party_dashboard_url(self):
        user = User.objects.create(username="Testuser")
        party = Party.objects.create(host=user, name="TestParty")
        response = client.get(f"/{user.id}/dashboard/{party.party_id}")
        self.assertEqual(response.status_code, 200)

# TODO: add tests
# TODO: home test user authenticated / not authenticated
# TODO: Host tests user authenticated / not authenticated
# TODO: Attending tests user authenticated / not authnticated
# TODO: Login tests