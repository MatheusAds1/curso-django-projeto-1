from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='my_user', password='pass')
        self.client.login(username='my_user', password='pass')

        response = self.client.get(reverse('authors:logout'), follow=True)

        self.assertIn('Invalid logout request',
                      response.content.decode('utf-8'))


    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(username='my_user', password='pass')
        self.client.login(username='my_user', password='pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'another_user'},
            follow=True)

        self.assertIn('Wrong user logout',
                      response.content.decode('utf-8'))


    def test_user_logout_successfully(self):
        User.objects.create_user(username='my_user', password='pass')
        self.client.login(username='my_user', password='pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'my_user'},
            follow=True
            )

        self.assertIn('You signed out',
                      response.content.decode('utf-8'))
