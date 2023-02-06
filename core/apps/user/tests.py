from django.test import TestCase
from .models import User
from django.test import Client
from rest_framework.authtoken.models import Token


class RegisterTestCase(TestCase):

    def setUp(self) -> None:
        self.register_user = User(
            username='test-01-name',
            first_name='test-01-name',
            last_name='test-01-name'
        )
        self.register_user.set_password('test-password')
        self.register_user.save()
        self.client = Client()

    def test_register_user(self):
        '''
            Check if register user is created by looking at the status code and verifying in the database
        '''
        context = {
            'username': 'test-username',
            'first_name': 'test-first-name',
            'last_name': 'test-last-name',
            'password': 'test-password'
        }
        response_register = self.client.post('/api/v1/user/signup', context)

        # Validate status and the creation of user
        user_query = User.objects.filter(username='test-username')
        self.assertEqual(user_query[0].username, 'test-username')
        self.assertEqual(user_query[0].first_name, 'test-first-name')
        self.assertEqual(response_register.status_code, 201)

    def test_login_user(self):
        '''
            Check if login endpoint returns status code of 200 and Token is not None
        '''

        response_login = self.client.post(
            '/api/v1/user/login', {'username': self.register_user.username, 'password': 'test-password'})
        self.assertEqual(response_login.status_code, 200)
        token = Token.objects.get(user=self.register_user)
        self.assertIsNotNone(token)
