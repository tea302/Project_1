from typing import Type, Any

from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from network.models import Contact, Product, TradeUnit


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model: Type[Contact] = Contact
        fields: str = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model: Type[Product] = Product
        fields: str = '__all__'


class RetailCreateSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(queryset=TradeUnit.objects.all())
    contact = ContactSerializer()
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    debt = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    def create(self, validated_data) -> Type[TradeUnit]:
        contact_data, product_data = validated_data.pop('contact'), validated_data.pop('products')
        contact_serializer = ContactSerializer(data=contact_data)
        contact_serializer.is_valid(raise_exception=True)
        contact = contact_serializer.save()
        trade_unit = TradeUnit.objects.create(contact=contact, **validated_data)
        trade_unit.products.set(product_data)
        trade_unit.debt = sum([product.price for product in trade_unit.products.all()])
        trade_unit.save()
        return trade_unit

    class Meta:
        model: Type[TradeUnit] = TradeUnit
        exclude: list = ['level']


class RetailSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField(required=False)
    contact = ContactSerializer(required=False)
    products = ProductSerializer(many=True, required=False)
    unit_type = serializers.SerializerMethodField(required=False)

    def get_unit_type(self, obj) -> Any:
        return obj.get_unit_type_display()

    def get_provider(self, obj) -> ReturnDict | None:
        if obj.provider:
            provider_serializer = self.__class__(obj.provider)
            return provider_serializer.data
        return None

    class Meta:
        model: Type[TradeUnit] = TradeUnit
        exclude: list = ['level']
        read_only_fields: list = ['debt']