from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.BaseSerializer):
    '''
        I use BaseSerializer in case it is required to change props in return dict
    '''

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            'price': instance.price
        }
