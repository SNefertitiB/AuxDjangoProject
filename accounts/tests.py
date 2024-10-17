from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse

# Create your tests here.
class ViewsTests(TestCase):
    def test_valid_signup(self):
        """
        Tests signup works with valid form input
        status code 302 for redirect after log in
        new User.object is created
        the new user has the right username
        the new user has the right email
        :return: None
        """
        username = 'TestUser'
        email = 'test@fakemail.com'
        password = 'better_password'
        valid_form_data = {'username': username,
                           'email': email,
                           'password1': password,
                           'password2': password}
        response = self.client.post(reverse("signup"), valid_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.username, username)
        self.assertEqual(new_user.email, email)

    def test_signup_username_taken(self):
        """
        test user already exists with username
        verify no new user is created
        status code 200 (reload sign up page)
        :return:None
        """
        existing_user = User.objects.create(username="Testuser",
                                            email='something@fakemail.com')
        username = existing_user.username
        email = 'test@fakemail.com'
        password = 'better_password'
        form_data = {'username': username,
                     'email': email,
                     'password1': password,
                     'password2': password}
        response = self.client.post(reverse("signup"), form_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        # self.assertEqual(len(messages), 1)   # TODO: work on these message based assertions
        # self.assertEqual(str(messages[1]), 'An account with that username already exists. Please log in or sign up with a different username')


    def test_signup_email_taken(self):
        """
        test user already exists with email
        verify no new user is created
        status code 200 (reload sign up page)
        :return:None
        """
        existing_user = User.objects.create(username="Testuser",
                                            email='something@fakemail.com')
        username = "A_user_name"
        email = existing_user.email
        password = 'better_password'
        form_data = {'username': username,
                     'email': email,
                     'password1': password,
                     'password2': password}
        response = self.client.post(reverse("signup"), form_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_signup_weak_password(self):
        """
        test signup if weak password is used
        no new user is created
        page is reloaded
        :return: None
        """
        username = 'TestUser'
        email = 'test@fakemail.com'
        password = 'password'
        form_data = {'username': username,
                           'email': email,
                           'password1': password,
                           'password2': password}
        response = self.client.post(reverse("signup"), form_data)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_signup_passwords_not_match(self):
        """
        test signup if weak password1 != password 2
        no new user is created
        page is reloaded
        :return: None
        """
        username = 'TestUser'
        email = 'test@fakemail.com'
        password1 = 'good_password'
        password2 = 'better_password'
        form_data = {'username': username,
                           'email': email,
                           'password1': password1,
                           'password2': password2}
        response = self.client.post(reverse("signup"), form_data)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_signup_logged_in_user(self):
        """
        test signup page if user already logged in
        redirect to home
        :return: None
        """
        user = User.objects.create(username='TestUser')
        self.client.force_login(user)
        response = self.client.post(reverse("signup"))
        self.assertEqual(response.status_code, 302)
