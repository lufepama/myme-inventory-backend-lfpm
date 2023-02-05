from rest_framework import serializers
from apps.warehouse.models import Warehouse
from apps.product.models import Product
from .models import WareProducts


class WareProductListSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'product': instance.get_product_data,
            'warehouseId': instance.warehouse.pk,
            'isAvailable': instance.is_available
        }


class WareProductSerializer(serializers.Serializer):
    warehouse_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def validate_warehouse_id(self, value):
        try:
            wr_query = Warehouse.objects.filter(pk=value)
            # Validate wr exists. If not, raise error with customized error message
            if (len(wr_query) > 0):
                return value
            else:
                raise serializers.ValidationError(
                    'Warehouse not found'
                )

        except:
            raise serializers.ValidationError(
                'Something went wrong with warehouse'
            )

    def validate_product_id(self, value):
        try:
            wr_query = Product.objects.filter(pk=value)

            # Validate prod exists. If not, raise error with customized error message
            if (len(wr_query) > 0):
                return value
            else:
                raise serializers.ValidationError(
                    'Product not found'
                )

        except:
            raise serializers.ValidationError(
                'Something went wrong with product id'
            )

    def validate_amount(self, value):

        if (value >= 0):
            return value
        else:
            raise serializers.ValidationError(
                'The amount must be positive integer value'
            )

    def create(self, validated_data):
        '''
            Create resource or increment amount prop in case it exists
        '''
        warehouse = Warehouse.objects.get(pk=validated_data['warehouse_id'])
        product = Product.objects.get(pk=validated_data['product_id'])
        amount = validated_data['amount']

        wrprod_query = WareProducts.objects.filter(
            product=product, warehouse=warehouse)
        if (len(wrprod_query) > 0):
            wrprod = wrprod_query.first()
            wrprod.amount += int(self.context['amount'])
            wrprod.save()
            return wrprod
        else:
            new_wareproduct = WareProducts(
                warehouse=warehouse,
                product=product,
                amount=amount
            )
            new_wareproduct.save()
            return new_wareproduct
