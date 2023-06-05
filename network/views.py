from typing import Type

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from network.filters import RetailCountryFilter
from network.models import TradeUnit
from network.serializer import RetailSerializer, RetailCreateSerializer


@extend_schema_view(
    create=extend_schema(
        description="Create new Retail Network",
        summary="Add Retail Network"
    ),
    retrieve=extend_schema(
        description="Get one Retail Network",
        summary="Get Retail Network"
    ),
    list=extend_schema(
        description="Get list of Retail Networks",
        summary="Get all Retail Networks"
    ),
    update=extend_schema(
        description="Full update of Retail Network",
        summary="Update Retail Network"
    ),
    partial_update=extend_schema(
        description="Partial update of Retail Network",
        summary="Partial update Retail Network"
    ),
    destroy=extend_schema(
        description="Delete Retail Network",
        summary="Delete Retail Network"
    ),
)
class RetailViewSet(ModelViewSet):
    queryset = TradeUnit.objects.all()
    default_serializer = RetailSerializer
    serializers: dict = {
        'create': RetailCreateSerializer
    }
    permission_classes: list = [IsAuthenticated]
    filter_backends: list = [DjangoFilterBackend]
    filterset_class: list = RetailCountryFilter

    def get_serializer_class(self) -> Type[RetailSerializer | RetailCreateSerializer]:
        return self.serializers.get(self.action, self.default_serializer)
