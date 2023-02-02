from rest_framework import serializers
from .models import Warehouse


class WarehouseSerializer(serializers.Serializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class WarehouseListSerializer(serializers.BaseSerializer):
    '''
        I use BaseSerializer in case it is required to change props in return dict
    '''

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            'address': instance.address,
            'phoneNumber': instance.phone_number,
            'country': instance.country
        }
