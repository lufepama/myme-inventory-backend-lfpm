from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .serializers import ProductSerializer, ProductListSerializer
from .models import Product


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_product(request, *args, **kwargs):
    try:
        data = request.data
        product_serializer = ProductSerializer(data=data)
        if (product_serializer.is_valid()):
            product_serializer.save()
            return Response({'success': True, 'message': 'Product created'}, status=status.HTTP_200_OK)

        return Response({'success': False, 'message': product_serializer.error_messages}, status=status.HTTP_200_OK)
    except:
        return Response({'success': False, 'message': 'Something went wrong...'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_products(request, *args, **kwargs):
    try:
        products = Product.objects.all()
        products_serializer = ProductListSerializer(products, many=True)
        return Response({'success': True, 'data': products_serializer.data}, status=status.HTTP_200_OK)

    except:
        return Response({'success': False, 'message': 'Something went wrong...'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_product(request, productId, *args, **kwargs):
    try:
        product_query = Product.objects.filter(id=productId)
        # If product exists, lets delete it
        if (len(product_query) > 0):
            product_query.first().delete()
            return Response({'success': True, 'message': 'Product deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'success': False, 'message': 'Something went wrong...'}, status=status.HTTP_403_FORBIDDEN)
