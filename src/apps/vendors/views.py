from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from helpers.responses import Responses
from helpers.request_validations import RequestValidator

from .serializers import VendorSerializer
from .models import Vendor
from apps.products.models import Product

class VendorsList( APIView, RequestValidator, Responses) :

    serializer_class = VendorSerializer
    permission_classes = []
    authentication_classes = []

    @csrf_exempt
    def get( self, request, format = None) :
        records = Vendor.get_all()
        serialized = VendorSerializer( records, many = True)
        if len( serialized.data) == 0 :
            return self._reply_no_content()
        return self._reply_get_ok( serialized.data)

    @csrf_exempt
    def post( self, request, format = None) :
        data = JSONParser().parse( request)
        vendor = data.get( 'vendor')
        products = data.get( 'products')
        if products == None :
            return self.create_vendor( vendor)
        return self.create_vendor_with_products( vendor, products)
        
    @csrf_exempt
    def delete( self, request, format = None) :
        data = JSONParser().parse( request).get( 'vendors')
        if not self._is_data_an_array_of_ids( data) :
            return self._reply_bad_request()
        errors = Vendor.destroy( data)
        return self._reply_ok()

    def create_vendor( self, vendor) :
        if not self._is_data_valid_for( vendor, Vendor.fields) :
            return self._reply_bad_request()
        errors = Vendor.create( vendor)
        return self._reply_created_or_failed( errors)

    def create_vendor_with_products( self, vendor, products) :
        if not (self._is_data_valid_for( vendor, Vendor.fields) 
            and self._is_data_an_array_with_fields( products, Product.fields)) :
            return self._reply_bad_request()
        errors = Vendor.create_with_products( vendor, products)
        return self._reply_created_or_failed( errors)


class VendorDetails( APIView, RequestValidator, Responses) :

    serializer_class = VendorSerializer
    permission_classes = []
    authentication_classes = []

    @csrf_exempt
    def get( self, request, primary_key, format = None) :
        if not Vendor.id_exists( primary_key) :
            return self._reply_not_found()
        serialized = VendorSerializer( Vendor.get( primary_key))
        return self._reply_get_ok( serialized.data)
    
    @csrf_exempt
    def put( self, request, primary_key, format = None) :
        if not Vendor.id_exists( primary_key) :
            return self._reply_not_found()
        data = JSONParser().parse( request).get( 'vendor')
        if not self._is_data_valid_for( data, Vendor.fields) :
            return self._reply_bad_request()
        errors = Vendor.find_and_try_to_update_with( primary_key, data) 
        return self._reply_updated_or_failed( errors)
        
    @csrf_exempt
    def delete( self, request, primary_key, format = None) :
        if not Vendor.id_exists( primary_key) :
            return self._reply_not_found()
        Vendor.destroy( [primary_key])
        return self._reply_ok()
        