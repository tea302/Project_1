from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from network.models import TradeUnit, Contact, Product
from network.serializer import ProductSerializer


@admin.register(TradeUnit)
class RetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'contact', 'products_', 'provider_', 'debt', 'unit_type', 'level')
    list_filter = ('contact__country', 'contact__city')
    actions = ['reset_debt']
    readonly_fields = ('level',)

    fieldsets = (
        ('Info', {
            'fields': ('title', 'unit_type', 'debt', 'level')
        }),
        ('Contact info', {
            'fields': ('contact',)
        }),
        ('Products', {
            'fields': ('products',)
        }),
        ('Provider', {
            'fields': ('provider',)
        })
    )

    def reset_debt(self, request, queryset) -> None:
        queryset.update(debt=0)

    @staticmethod
    def products_(obj):
        products = ProductSerializer(obj.products, many=True).data
        product_list = []
        for i, product in enumerate(products):
            product_url = reverse('admin:chain_product_change', args=[product['id']])
            product_link = format_html('<a href="{}">{}</a>', product_url, product['title'])
            product_list.append(f"{i + 1}. {product_link}")
        return format_html("<br>".join(product_list))

    def provider_(self, obj):
        if obj.provider:
            url = reverse('admin:chain_tradeunit_change', args=[obj.provider.id])
            return format_html('<a href="{}">{}</a>', url, obj.provider.title)
        return None

    provider_.short_description = 'Provider'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'country', 'city', 'street', 'number')
    list_filter = ('country', 'city')

    fieldsets = (
        ('Info', {
            'fields': ('country', 'city', 'street', 'number')
        }),
        ('Email address', {
            'fields': ('email',)
        })
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'model', 'release', 'price')
    list_filter = ('model',)

    fieldsets = (
        ('Info', {
            'fields': ('title', 'model')
        }),
        ('Price', {
            'fields': ('price',)
        }),
        ('Release date', {
            'fields': ('release',)
        })
    )