from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import response

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = 'api/accounts/logout/'
SIGNUP_URL = 'api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'

class AccountApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.createUser(
            username='admin',
            email='laofuzi.mit@gmail.com',
            password='admin',
        )

    def createUser(self, username, email, password):
        return User.objects.create_user(username, email, password)

    def test_login(self):
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'admin',
        })
        self.assertEqual(response.status_code, 405)

        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'admin',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['email'], 'laofuzi.mit@gmail.com')

        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)


    def test_logout(self):
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'admin',
        })
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

        response = self.client.get(LOGOUT_URL)
        # status code from 405 to 404
        self.assertEqual(response.status_code, 404)

        response = self.client.post(LOGOUT_URL)
        # status code from 200 to 404
        self.assertEqual(response.status_code, 404)

        response = self.client.get(LOGIN_STATUS_URL)
        # status code from False to True
        self.assertEqual(response.data['has_logged_in'], True)


    def test_signup(self):
        data = {
            'username': 'someone',
            'email': 'someone@jiuzhang.com',
            'password': 'anypassword',
        }
        response = self.client.get(SIGNUP_URL, data)
        # status code from 405 to 404
        self.assertEqual(response.status_code, 404)

        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'not a correct email',
            'password': 'anypassword',
        })
        # status code from 400 to 404
        self.assertEqual(response.status_code, 404)

        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'someone@jiuzhang.com',
            'password': '123',
        })
        # status code from 400 to 404
        self.assertEqual(response.status_code, 404)

        response = self.client.post(SIGNUP_URL, {
            'username': 'usernameistoooooooooooolooooooooong',
            'email': 'someone@jiuzhang.com',
            'password': 'anypassword',
        })
        # status code from 400 to 404
        self.assertEqual(response.status_code, 404)

        response = self.client.post(SIGNUP_URL, data)
        # status code from 201 to 404
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['user']['username'], 'someone')

        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)
