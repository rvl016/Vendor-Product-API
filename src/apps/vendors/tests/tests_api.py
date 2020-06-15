from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.views import status

from ..models import Vendor
from ..serializers import VendorSerializer
from ..views import VendorsList, VendorDetails

class VendorListAPITestCase( APITestCase) :
      
    def setUp( self) :
        self.client = APIClient()
        self.vendor1 = Vendor.create( { 'name': "MyCompany", 
            'cnpj': "55.555.555/0000-00" })
        self.vendor2 = Vendor.create( { 'name': "Bradoo", 
            'cnpj': "26.402.093/0001-74", 'city': "São Paulo" })
        self.vendor3 = Vendor.create( { 'name': "Ravi Inc.", 
            'cnpj': "26.407.093/0401-74", 'city': "Jaú" })
    
    def test_get( self) :
        response = self.client.get( reverse( "vendors"))
        expected = Vendor.objects.all()
        serialized = VendorSerializer( expected, many = True)
        self.assertEqual( response.json()['data'], serialized.data)
        self.assertEqual( response.status_code, status.HTTP_200_OK)

    def test_post_bad_requests( self) :
        response = self.client.post( reverse( "vendors"), {}, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post( reverse( "vendors"), {
            'vendor': {
                'nami': "Mai nami",
                'name': "My name"
            }
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_invalid( self) :
        response = self.client.post( reverse( "vendors"), {
            'vendor': {
                'name': "Django Inc.",
                'cnpj': "00.006660.000/0000-10"
            }
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertNotEqual( response.json().get( 'errors'), None)     
        
    def test_correct_post( self) :
        response = self.client.post( reverse( "vendors"), {
            'vendor': {
                'name': "Django Inc.",
                'cnpj': "00.000.000/0000-10"
            }
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_201_CREATED)
        self.assertEqual( Vendor.objects.filter( cnpj = "00.000.000/0000-10").count(), 1)

    def test_incorrect_delete( self) :        
        response = self.client.delete( reverse( "vendors"), {
            'vendors': 1
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_correct_delete( self) :        
        response = self.client.delete( reverse( "vendors"), {
            'vendors': [
                Vendor.objects.first().id
            ]
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_200_OK)
        self.assertEqual( Vendor.objects.all().count(), 2)


class VendoDetailsAPITestCase( APITestCase) :
      
    def setUp( self) :
        self.client = APIClient()
        self.vendor1 = Vendor.objects.create( name = "MyCompany", 
            cnpj = "55.555.555/0000-00")
        self.vendor2 = Vendor.objects.create( name = "Bradoo", 
            cnpj = "26.402.093/0001-74", city = "São Paulo")
        self.vendor3 = Vendor.objects.create( name = "Ravi Inc.", 
            cnpj = "26.407.093/0401-74", city = "Jaú")

    def test_invalid_get( self) :
        response = self.client.get( reverse( "vendor-details", 
            args = ( 99999999999999999999, )))
        self.assertEqual( response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_get( self) :
        response = self.client.get( reverse( "vendor-details", 
            args = ( self.vendor1.id, )))
        expected = Vendor.objects.get( id = self.vendor1.id)
        serialized = VendorSerializer( expected)
        self.assertEqual( response.json()['data'], serialized.data)
        self.assertEqual( response.status_code, status.HTTP_200_OK)

    def test_put_bad_requests( self) :
        response = self.client.put( reverse( "vendor-details", 
            args = ( self.vendor1.id, )), {
            'vendor': {
                'nami': "Mai nami",
                'name': "My name"
            }
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_invalid( self) :
        response = self.client.put( reverse( "vendor-details", 
            args = ( self.vendor1.id, )), {
            'vendor': {
                'cnpj': "894892395"
            }
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_put_valid( self) :
        id = self.vendor1.id
        response = self.client.put( reverse( "vendor-details", 
            args = ( id, )), {
            'vendor': {
                'name': "New name",
                'city': "New city"
            }
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_200_OK)
        self.vendor1.refresh_from_db()
        self.assertEqual( self.vendor1.id, id)
        self.assertEqual( self.vendor1.name, "New name")
        self.assertEqual( self.vendor1.city, "New city")
        self.assertEqual( self.vendor1.cnpj, "55.555.555/0000-00")

    def test_correct_delete( self) :        
        id = self.vendor1.id
        response = self.client.delete( reverse( "vendor-details",
            args = ( id, )))
        self.assertEqual( response.status_code, status.HTTP_200_OK)
        response = self.client.delete( reverse( "vendor-details",
            args = ( id, )))
        self.assertEqual( response.status_code, status.HTTP_404_NOT_FOUND)