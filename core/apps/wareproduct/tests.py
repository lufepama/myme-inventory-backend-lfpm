from django.test import TestCase
from apps.user.models import User
from apps.warehouse.models import Warehouse
from apps.product.models import Product
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

# Create your tests here.


class WareProductTestCase(TestCase):

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

        warehouse = {
            'name': 'test-warehouse-name',
            'description': 'test-warehouse-description',
            'address': 'test-warehouse-address',
            'phone_number': '34234235',
            'country': 'test-country',
        }

        self.api_client.post(
            '/api/v1/warehouse/create', warehouse)

        product = {
            'name': 'test-product-name',
            'description': 'test-product-description',
            'price': 2
        }
        self.product = self.api_client.post(
            '/api/v1/product/create', product)

        self.query_warehouse = Warehouse.objects.get(
            name='test-warehouse-name',
            description='test-warehouse-description',
        )
        self.query_product = Product.objects.get(
            name='test-product-name',
            description='test-product-description',
        )

    def test_create_product_in_warehouse(self):
        '''
            Test the creation of a product in a given warehouse
        '''
        # Initializes the data to send in request
        context = {
            'warehouseId': self.query_warehouse.pk,
            'productId': self.query_product.pk,
            'amount': 2
        }

        # Make request
        response_create_prod_warehouse = self.api_client.post(
            '/api/v1/wareproduct/create-product', context)
        # Status code must be 201
        self.assertEquals(response_create_prod_warehouse.status_code, 201)

    def test_get_warehouse_products(self):
        '''
            Test if products from a warehouse are fetched
        '''
        context = {
            'warehouseId': self.query_warehouse.pk,
            'productId': self.query_product.pk,
            'amount': 2
        }
        # Add product in warehouse
        response_create_prod_warehouse = self.api_client.post(
            '/api/v1/wareproduct/create-product', context)
        # Recover the wareproduct id created above
        wareproduct_id = response_create_prod_warehouse.json()['data']['id']

        # Get products from warehouse
        response_get_prod_warehouse = self.api_client.get(
            f'/api/v1/wareproduct/get-products/{wareproduct_id}')

        # Status code must be 200
        self.assertEquals(response_get_prod_warehouse.status_code, 200)

        # Data returned from request must be an array containing the the information below
        self.assertEquals(response_get_prod_warehouse.json()['data'],
                          [{'id': 1,
                            'isAvailable': True,
                            'product': {'amount': 2,
                                        'description': 'test-product-description',
                                        'id': 1,
                                        'name': 'test-product-name',
                                        'price': 2.0},
                              'warehouseId': 1}])

    def test_delete_warehouse_product(self):
        '''
            Test if an product of an warehouse is deleted successgully
        '''
        context = {
            'warehouseId': self.query_warehouse.pk,
            'productId': self.query_product.pk,
            'amount': 2
        }
        # Add product in warehouse
        response_create_prod_warehouse = self.api_client.post(
            '/api/v1/wareproduct/create-product', context)

        # Recover the wareproduct id created above
        wareproduct_id = response_create_prod_warehouse.json()['data']['id']

        # Make the delete request
        response_delete_prod_warehouse = self.api_client.delete(
            f'/api/v1/wareproduct/delete-product/{wareproduct_id}')

        # The status code must be 200 as it is stablished in the method
        self.assertEquals(response_delete_prod_warehouse.status_code, 200)

    def test_update_amount_warehouse_product(self):
        '''
            Test if update amount action is successfully requested 
        '''
        context = {
            'warehouseId': self.query_warehouse.pk,
            'productId': self.query_product.pk,
            'amount': 2
        }
        # Add product in warehouse
        response_create_prod_warehouse = self.api_client.post(
            '/api/v1/wareproduct/create-product', context)

        # Recover the wareproduct id created above
        wareproduct_id = response_create_prod_warehouse.json()['data']['id']

        context_update = {
            'wrProductId': wareproduct_id,
            'amount': 10
        }

        response_update_amount_prod_warehouse = self.api_client.put(
            '/api/v1/wareproduct/update-product-amount', context_update)

        # The status code must be 200 as it is stablished in the method
        self.assertEquals(
            response_update_amount_prod_warehouse.status_code, 200)

    def test_create_multiple_warehouse_product(self):
        '''
            Test if a product can be added into multiple warehouses. For 
            simplicity only three warehouses will be considered
        '''
        warehouse = {
            'name': 'test-warehouse-name',
            'description': 'test-warehouse-description',
            'address': 'test-warehouse-address',
            'phone_number': '34234235',
            'country': 'test-country',
        }

        # Create three warehouses as product is already created in setUp method
        response_warehouse_1 = self.api_client.post(
            '/api/v1/warehouse/create', warehouse)
        response_warehouse_2 = self.api_client.post(
            '/api/v1/warehouse/create', warehouse)
        response_warehouse_3 = self.api_client.post(
            '/api/v1/warehouse/create', warehouse)

        # Recover warehouse ids from response data of each one
        response_warehouse_1_id = response_warehouse_1.json()['data']['id']
        response_warehouse_2_id = response_warehouse_2.json()['data']['id']
        response_warehouse_3_id = response_warehouse_3.json()['data']['id']

        context = {
            'productId': self.product.json()['data']['id'],
            'warehouseIdList': [response_warehouse_1_id, response_warehouse_2_id, response_warehouse_3_id],
            'amount': '10'
        }

        # Make request
        response_add_product_warehouses = self.api_client.post(
            '/api/v1/wareproduct/create-multiple-product', context)

        # Status code must be 201
        self.assertEquals(response_add_product_warehouses.status_code, 201)

    def test_delete_multiple_warehouse_product(self):
        '''
            Test if product is deleted from a list of warehouses. For 
            simplicity only three warehouses will be considered
        '''
        warehouse = {
            'name': 'test-warehouse-name',
            'description': 'test-warehouse-description',
            'address': 'test-warehouse-address',
            'phone_number': '34234235',
            'country': 'test-country',
        }

        # Create three warehouses as product is already created in setUp method
        response_warehouse_1 = self.api_client.post(
            '/api/v1/warehouse/create', warehouse)
        response_warehouse_2 = self.api_client.post(
            '/api/v1/warehouse/create', warehouse)
        response_warehouse_3 = self.api_client.post(
            '/api/v1/warehouse/create', warehouse)

        # Recover warehouse ids from response data of each one
        response_warehouse_1_id = response_warehouse_1.json()['data']['id']
        response_warehouse_2_id = response_warehouse_2.json()['data']['id']
        response_warehouse_3_id = response_warehouse_3.json()['data']['id']

        context = {
            'productId': self.product.json()['data']['id'],
            'warehouseIdList': [response_warehouse_1_id, response_warehouse_2_id, response_warehouse_3_id],
            'amount': '10'
        }

        # Make add product request
        response_add_product_warehouses = self.api_client.post(
            '/api/v1/wareproduct/create-multiple-product', context)

        context_delete = {
            'warehouseIdList': [response_warehouse_1_id, response_warehouse_2_id, response_warehouse_3_id],
            'productId': self.product.json()['data']['id']
        }

        # Make delete product request
        response_delete_product_warehouses = self.api_client.delete(
            '/api/v1/wareproduct/delete-multiple-product', context_delete)

        self.assertEquals(response_delete_product_warehouses.status_code, 200)
