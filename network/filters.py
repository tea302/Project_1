
from typing import Type

from django_filters.rest_framework import filters

from network.models import TradeUnit


class RetailCountryFilter(filters.FilterSet):
    city = filters.CharFilter(field_name='contact__city')

    class Meta:
        model: Type[TradeUnit] = TradeUnit
        fields: list = ['city']
