from rest_framework import serializers
from apps.vendors.serializers import VendorSerializer

from .models import Product

class VendorDetailsProductSerializer( serializers.ModelSerializer) :

    vendor = VendorSerializer( read_only = True)

    class Meta :
        model = Product
        fields = ['vendor', 'id', 'name', 'code', 'price']
        read_only_fields = ['id', 'vendor']
    

class VendorProductSerializer( serializers.ModelSerializer) :

    vendor_id = serializers.PrimaryKeyRelatedField( 
        source = 'vendor', read_only = True)
    vendor_name = serializers.StringRelatedField( source = 'vendor', 
        read_only = True)

    class Meta :
        model = Product
        fields = ['id', 'vendor_id', 'vendor_name', 'name', 'code', 'price']
        read_only_fields = ['id', 'vendor_id', 'vendor_name']


class ProductSerializer( serializers.ModelSerializer) :

    class Meta :
        model = Product
        fields = ['id', 'name', 'code', 'price']
        read_only_fields = ['id']
    