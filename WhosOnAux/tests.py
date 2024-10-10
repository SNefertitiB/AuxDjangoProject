from django.test import TestCase
from django.test import Client
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth.models import User
from WhosOnAux.models import Party
from .forms import NewPartyForm

import WhosOnAux.views
# Create your tests here.

REDIRECT_302 = 302   # "Found" or "Moved Temporarily" |Temporarily relocate a site to a new URL
OK_200 = 200         # GET A resource was retrieved and included in the response body
client = Client()
# request = HttpRequest
class URLsTests(TestCase):
    def test_landing_url(self):
        response = client.get("")
        self.assertEqual(response.status_code, 200)

    def test_user_home_url(self):
        user = User.objects.create(username="Testuser")
        response = client.get(f"/home/")
        self.assertEqual(response.status_code, 200)

    def test_user_hosting_url(self):
        user = User.objects.create(username="Testuser")
        response = client.get(f"/hosting/")
        self.assertEqual(response.status_code, 200)

    def test_create_new_party_url(self):
        user = User.objects.create(username="Testuser")
        self.client.force_login(user)
        form_data = {"party_name": "A party name",
                     "description": "short description of party"}
        response = self.client.post(reverse("create_new_party"), form_data)
        self.assertEqual(response.status_code, 302)

    def test_user_attending_url(self):
        user = User.objects.create(username="Testuser")
        response = client.get(f"/attending/")
        self.assertEqual(response.status_code, 200)

    def test_attending_party_url(self):
        user = User.objects.create(username="Testuser")
        party = Party.objects.create(host=user, name="TestParty")
        response = client.get(f"/attending/{party.party_id}")
        self.assertEqual(response.status_code, 200)

    def test_party_dashboard_url(self):
        user = User.objects.create(username="Testuser")
        party = Party.objects.create(host=user, name="TestParty")
        response = client.get(f"/dashboard/{party.party_id}")
        self.assertEqual(response.status_code, 200)


class NewPartyFormTests(TestCase):
    def test_valid_form(self):
        name = "A party name"
        description = "short description of party"
        form_data = {"party_name": name, "description": description}
        form = NewPartyForm(data=form_data)
        self.assertTrue(form.is_valid())

# TODO: add tests
# TODO: home test user authenticated / not authenticated
# TODO: Host tests user authenticated / not authenticated
# TODO: Attending tests user authenticated / not authnticated
# TODO: Login tests
