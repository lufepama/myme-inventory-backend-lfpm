from django.test import TestCase
from apps.user.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import Product

# Create your tests here.


class ProductTestCase(TestCase):

    def setUp(self) -> None:
        self.register_user = User(
            username='test-01-name',
            first_name='test-01-name',
            last_name='test-01-name'
        )
        self.register_user.set_password('test-password')
        self.register_user.save()
        self.client.post('/api/v1/user/login',
                         {'username': self.register_user.username, 'password': 'test-password'})
        self.user_token = Token.objects.get(user=self.register_user)
        self.api_client = APIClient()
        self.api_client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user_token.key)

    def test_create_product(self):
        '''
            Check if product resource is created. The status code must be 201
        '''
        product = {
            'name': 'test-product-name',
            'description': 'test-product-description',
            'price': 2
        }
        response_create = self.api_client.post(
            '/api/v1/product/create', product)
        self.assertEqual(response_create.status_code, 201)

        query_product = Product.objects.filter(
            name=product['name'], description=product['description'])
        self.assertEqual(query_product[0].name, 'test-product-name')
        self.assertEqual(
            query_product[0].description, 'test-product-description')

    def test_get_products(self):
        '''
            Check if product list are fetched successfully
        '''
        response_fetch = self.api_client.get('/api/v1/product/get-products')
        self.assertEqual(response_fetch.status_code, 200)

        # The data must be an empty array
        self.assertEquals(response_fetch.json()['data'], [])

    def test_delete_product(self):
        '''
            Check if delete product is deleted from database
        '''
        product = {
            'name': 'test-product-name',
            'description': 'test-product-description',
            'price': 2
        }
        # Create product
        response_create = self.api_client.post(
            '/api/v1/product/create', product)
        # Recover id from data returned in previous request
        product_created_id = response_create.json()['data']['id']
        response_delete = self.api_client.delete(
            f'/api/v1/product/delete/{product_created_id}')
        # Status code must be 200
        self.assertEqual(response_delete.status_code, 200)
