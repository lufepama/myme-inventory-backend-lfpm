from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .serializers import WareProductSerializer, WareProductListSerializer
from apps.product.models import Product
from .models import WareProducts
from apps.warehouse.models import Warehouse


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_warehouse_product(request, *args, **kwargs):
    '''
        Manages the creation of a single warehouse-product assigning an certain amount of product.
        It makes use of serializer to create the resource where some custom validations are run
    '''
    try:
        # Get data from body
        data = request.data
        # Convert data from camelcase to snakecase (python friendly notation)
        ser_data = {
            'warehouse_id': data['warehouseId'],
            'product_id': data['productId'],
            'amount': data['amount']
        }

        wareproduct_serializer = WareProductSerializer(
            data=ser_data, context=ser_data)
        if (wareproduct_serializer.is_valid()):
            wareproduct_serializer.save()
            return Response({'success': True, 'message': 'Wareproduct created'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': wareproduct_serializer.errors}, status=status.HTTP_200_OK)

    except Exception as e:
        print({e})
        return Response({'success': False, 'message': 'Something went wrong'}, status=status.HTTP_502_BAD_GATEWAY)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_multiple_warehouse_product(request, *args, **kwargs):
    '''
        Manages the creation or update of warehouse-product, attending to a given product amount 
        If resource already exists, it will add the amount to the previous one
    '''
    try:
        data = request.data
        product_id = data['productId']
        product_amount = data['amount']
        warehouse_id_list = data['warehouseIdList']
        product_query = Product.objects.filter(pk=product_id)
        if (len(product_query) > 0):
            for id in warehouse_id_list:
                warehouse_query = Warehouse.objects.filter(pk=id)
                if (len(warehouse_query) > 0):
                    wrproduct_query = WareProducts.objects.filter(
                        warehouse=warehouse_query.first()).filter(product=product_query.first())
                    if (len(wrproduct_query) > 0):
                        wrproduct = wrproduct_query.first()
                        wrproduct.amount += product_amount
                        wrproduct.save()
                    else:
                        new_wareproduct = WareProducts(
                            warehouse=warehouse_query.first(),
                            product=product_query.first(),
                            amount=product_amount
                        )
                        new_wareproduct.save()

            return Response({'success': True, 'message': 'Product added to warehouses successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response({'success': False, 'message': 'Something went wrong'}, status=status.HTTP_502_BAD_GATEWAY)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_warehouse_products(request, *args, **kwargs):
    ''''
        Returns all products placed in a given warehouse. A serializer is used to return the data in 
        personalized format
    '''
    try:
        # Get data from body
        data = request.data
        warehouse_id = data['warehouseId']
        wr_query = Warehouse.objects.filter(pk=warehouse_id)
        if (len(wr_query)):
            wrproduct_query = WareProducts.objects.filter(
                warehouse=wr_query.first())
            wareproduct_serializer = WareProductListSerializer(
                wrproduct_query, many=True)
            return Response({'success': True, 'message': 'Warehouse products fetched', 'data': wareproduct_serializer.data}, status=status.HTTP_200_OK)

        return Response({'success': False, 'message': 'Warehouse not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print(e)
        return Response({'success': False, 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_warehouse_product(request, *args, **kwargs):
    '''
        Manages the removal of a warehouse
    '''
    try:
        # Get data from body
        wrproduct_id = request.data['wrProductId']

        wr_quer = WareProducts.objects.filter(pk=wrproduct_id)
        if (len(wr_quer) > 0):
            wr_quer.first().delete()
            return Response({'success': True, 'message': 'Product deleted from warehouse successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'Warehouse not found'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'success': False, 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_multiple_warehouse_product(request, *args, **kwargs):
    '''
        Manages the removal warehouse products
    '''
    try:
        # Get data from body
        data = request.data
        product_id = data['productId']
        warehouse_id_list = data['warehouseIdList']
        product_query = Product.objects.filter(pk=product_id)
        if (len(product_query) > 0):
            for id in warehouse_id_list:
                warehouse_query = Warehouse.objects.filter(pk=id)
                if (len(warehouse_query) > 0):
                    wrproduct_query = WareProducts.objects.filter(
                        warehouse=warehouse_query.first()).filter(product=product_query.first())
                    if (len(wrproduct_query) > 0):
                        wrproduct_query.first().delete()

            return Response({'success': True, 'message': 'Product deleted from warehouses successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response({'success': False, 'message': 'Something went wrong'}, status=status.HTTP_502_BAD_GATEWAY)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_amount_warehouse_product(request, *args, **kwargs):
    '''
        Updates the amount prop of product in a warehouse
    '''
    try:
        # Get data from body
        data = request.data
        wrproduct_id = data['wrProductId']
        amount = data['amount']
        wr_quer = WareProducts.objects.filter(pk=wrproduct_id)
        if (len(wr_quer) > 0):
            wrproduct = wr_quer.first()
            wrproduct.amount = amount
            wrproduct.save()
            return Response({'success': True, 'message': 'Warehouse product amount updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'Warehouse product not found'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'success': False, 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
