from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from helpers.responses import Responses
from helpers.request_validations import RequestValidator

from .serializers import ProductSerializer, VendorProductSerializer
from .models import Product
from apps.vendors.models import Vendor

class AllProductsList( APIView, RequestValidator, Responses) :

    serializer_class = VendorProductSerializer
    permission_classes = []
    authentication_classes = []

    @csrf_exempt
    def get( self, request, format = None) :
        records = Product.get_all()
        serialized = VendorProductSerializer( records, many = True)
        if len( serialized.data) == 0 :
            return self._reply_no_content()
        return self._reply_get_ok( serialized.data)
    
    @csrf_exempt
    def delete( self, request, format = None) :
        data = JSONParser().parse( request).get( 'products')
        if not self._is_data_an_array_of_ids( data) :
            return self._reply_bad_request()
        errors = Product.destroy( data)
        return self._reply_ok()


class VendorProductsList( APIView, RequestValidator, Responses) :

    serializer_class = ProductSerializer
    permission_classes = []
    authentication_classes = []

    @csrf_exempt
    def get( self, request, vendor_id, format = None) :
        if not Vendor.id_exists( vendor_id) :
            return self._reply_not_found()
        records = Product.get_all_from_vendor( vendor_id)
        serialized = ProductSerializer( records, many = True)
        if len( serialized.data) == 0 :
            return self._reply_no_content()
        return self._reply_get_ok( serialized.data)

    @csrf_exempt
    def post( self, request, vendor_id, format = None) :
        if not Vendor.id_exists( vendor_id) :
            return self._reply_not_found()
        data = JSONParser().parse( request)
        if data.get( 'product') :
            return self.create_one( data, vendor_id)
        return self.create_multiple( data, vendor_id)
    
    def create_one( self, data, vendor_id) :
        data = data.get( 'product')
        if not self._is_data_valid_for( data, Product.fields) :
            return self._reply_bad_request()
        errors = Product.create( data, vendor_id)
        return self._reply_created_or_failed( errors)
        
    def create_multiple( self, data, vendor_id) :
        data = data.get( 'products')
        if not self._is_data_an_array_with_fields( data, Product.fields) :
            return self._reply_bad_request()
        errors = Product.create_multiple( data, vendor_id)
        return self._reply_created_or_failed( errors)


class ProductDetails( APIView, RequestValidator, Responses) :

    serializer_class = VendorProductSerializer
    permission_classes = []
    authentication_classes = []
    
    @csrf_exempt
    def get( self, request, primary_key, format = None) :
        if not Product.id_exists( primary_key) :
            return self._reply_not_found()
        serialized = VendorProductSerializer( Product.get_by_id( primary_key))
        return self._reply_get_ok( serialized.data)
    
    @csrf_exempt
    def put( self, request, primary_key, format = None) :
        if not Product.id_exists( primary_key) :
            return self._reply_not_found()
        data = JSONParser().parse( request).get( 'product')
        if not self._is_data_valid_for( data, Product.fields) :
            return self._reply_bad_request()
        errors = Product.find_and_try_to_update_with( primary_key, data) 
        return self._reply_updated_or_failed( errors)
        
    @csrf_exempt
    def delete( self, request, primary_key, format = None) :
        if not Product.id_exists( primary_key) :
            return self._reply_not_found()
        Product.destroy( [primary_key])
        return self._reply_ok()