from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from helpers.responses import Responses
from helpers.request_validations import RequestValidator

from .serializers import VendorSerializer
from .models import Vendor

class VendorsList( APIView, RequestValidator, Responses) :

    serializer_class = VendorSerializer
    permission_classes = []
    authentication_classes = []

    @csrf_exempt
    def get( self, request, format = None) :
        records = Vendor.get_all()
        serialized = VendorSerializer( records, many = True)
        return self._reply_get_ok( serialized.data)

    @csrf_exempt
    def post( self, request, format = None) :
        data = JSONParser().parse( request).get( 'vendor')
        if not self._is_data_valid_for( data, Vendor.fields) :
            return self._reply_bad_request()
        errors = Vendor.create( data)
        return self._reply_created_or_failed( errors)
    
    @csrf_exempt
    def delete( self, request, format = None) :
        data = JSONParser().parse( request).get( 'vendors')
        if not self._is_data_an_array_of_ids( data) :
            return self._reply_bad_request()
        errors = Vendor.destroy( data)
        return self._reply_ok()


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
        