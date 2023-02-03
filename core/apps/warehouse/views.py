from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .serializers import WarehouseSerializer, WarehouseListSerializer
from .models import Warehouse


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_warehouse(request, *args, **kwargs):
    '''
        Manages the creation of a new warehouse
    '''
    try:
        # Get data from body
        data = request.data
        warehouse_serializer = WarehouseSerializer(data=data)
        if (warehouse_serializer.is_valid()):
            warehouse_serializer.save()
            return Response({'success': True, 'message': 'Warehouse created', 'data': warehouse_serializer.data}, status=status.HTTP_200_OK)

        return Response({'success': False, 'message': warehouse_serializer.error_messages}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'success': False, 'message': 'Something went wrong...'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_warehouses(request, *args, **kwargs):
    '''
        Manages the return of the list of warehouses saved in ddbb
    '''
    try:
        warehouses = Warehouse.objects.all()
        warehousees_serializer = WarehouseListSerializer(warehouses, many=True)
        return Response({'success': True, 'data': warehousees_serializer.data}, status=status.HTTP_200_OK)

    except:
        return Response({'success': False, 'message': 'Something went wrong...'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_warehouse(request, warehouseId, *args, **kwargs):
    '''
        Manages the removal of a single warehouse attending to its warehouseId
    '''
    try:
        warehouse_query = Warehouse.objects.filter(id=warehouseId)
        # If Warehouse exists, lets delete it
        if (len(warehouse_query) > 0):
            warehouse_query.first().delete()
            return Response({'success': True, 'message': 'Warehouse deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'Warehouse not found'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'success': False, 'message': 'Something went wrong...'}, status=status.HTTP_403_FORBIDDEN)
