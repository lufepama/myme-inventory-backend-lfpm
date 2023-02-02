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
    try:
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


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_warehouse_products(request, *args, **kwargs):

    try:
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
        return Response({'success': True, 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_warehouse_product(request, *args, **kwargs):
    pass
