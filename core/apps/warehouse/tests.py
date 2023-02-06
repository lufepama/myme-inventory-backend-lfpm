from django.test import TestCase
from apps.user.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import Warehouse

# Create your tests here.


class WarehouseTestCase(TestCase):

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

    def test_create_warehouse(self):
        '''
            Check if warehouse resource is created. The status code must be 201
        '''
        warehouse = {
            'name': 'test-warehouse-name',
            'description': 'test-warehouse-description',
            'address': 'test-warehouse-address',
            'phone_number': '34234235',
            'country': 'test-country',
        }
        response_create = self.api_client.post(
            '/api/v1/warehouse/create', warehouse)
        self.assertEqual(response_create.status_code, 201)

        query_warehouse = Warehouse.objects.filter(
            name=warehouse['name'], description=warehouse['description'])
        self.assertEqual(query_warehouse[0].name, 'test-warehouse-name')
        self.assertEqual(
            query_warehouse[0].description, 'test-warehouse-description')

    def test_get_warehouses(self):
        '''
            Check if warehouse list are fetched successfully
        '''
        response_fetch = self.api_client.get(
            '/api/v1/warehouse/get-warehouses')
        self.assertEqual(response_fetch.status_code, 200)

        # The data must be an empty array
        self.assertEquals(response_fetch.json()['data'], [])

    def test_delete_warehouse(self):
        '''
            Check if delete warehouse is deleted from database
        '''
        warehouse = {
            'name': 'test-warehouse-name',
            'description': 'test-warehouse-description',
            'address': 'test-warehouse-address',
            'phone_number': '34234235',
            'country': 'test-country',
        }
        # Create warehouse
        response_create = self.api_client.post(
            '/api/v1/warehouse/create', warehouse)
        # Recover id from data returned in previous request
        warehouse_created_id = response_create.json()['data']['id']
        response_delete = self.api_client.delete(
            f'/api/v1/warehouse/delete/{warehouse_created_id}')
        # Status code must be 200
        self.assertEqual(response_delete.status_code, 200)
