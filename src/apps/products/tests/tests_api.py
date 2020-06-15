from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.views import status

from apps.vendors.models import Vendor
from ..models import Product
from ..serializers import ProductSerializer, VendorProductSerializer
from ..views import AllProductsList, VendorProductsList, ProductDetails

class GenData() :
    
    def gen( self) :
        self.vendor1 = Vendor.objects.create( name = "MyCompany", 
            cnpj = "55.555.555/0000-00")
        self.vendor2 = Vendor.objects.create( name = "Bradoo", 
            cnpj = "26.402.093/0001-74", city = "São Paulo")
        self.vendor3 = Vendor.objects.create( name = "Ravi Inc.", 
            cnpj = "26.407.093/0401-74", city = "Jaú")

        self.product10 = Product.objects.create( vendor = self.vendor1, 
            name = "Piece of Cake", code = '010101010101', 
            price = Product.decimize_it( 0.0))
        self.product11 = Product.objects.create( vendor = self.vendor1, 
            name = "AK47", code = '111111111111', 
            price = Product.decimize_it( 666))
        self.product12 = Product.objects.create( vendor = self.vendor1, 
            name = "The awnser", code = '222222222222',
            price = Product.decimize_it( 42))
        self.product13 = Product.objects.create( vendor = self.vendor1, 
            name = "Bitcoin", code = '333333333333',
            price = Product.decimize_it( 25000))
        self.product20 = Product.objects.create( vendor = self.vendor2, 
            name = "The awnser", code = '444444444444',
            price = Product.decimize_it( 42))
        self.product21 = Product.objects.create( vendor = self.vendor2, 
            name = "Bitcoin", code = '555555555555',
            price = Product.decimize_it( 25000))


class AllProductsListAPITestCase( APITestCase, GenData) :
      
    def setUp( self) :
        self.client = APIClient()
        self.gen()


    def test_get_works( self) :
        response = self.client.get( reverse( "all-products"))
        expected = Product.get_all()
        serialized = VendorProductSerializer( expected, many = True)
        self.assertEqual( response.json()['data'], serialized.data)
        self.assertEqual( response.status_code, status.HTTP_200_OK)
        
    def test_delete( self) :
        response = self.client.delete( reverse( "all-products"), {
            'products': [
                self.product10.id,
                self.product21.id
            ]
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_200_OK)
        self.assertEqual( Product.objects.all().count(), 4)


class VendorProductsListAPITestCase( APITestCase, GenData) :

    def setUp( self) :
        self.client = APIClient()
        self.gen()


    def test_get_for_non_existent_vendor_returns_not_found( self) :
        response = self.client.get( reverse( "vendor-products", 
            args = ( 99999, )))
        self.assertEqual( response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_for_vendor_with_no_products_returns_no_content( self) :
        response = self.client.get( reverse( "vendor-products", 
            args = ( self.vendor3.id, )))
        self.assertEqual( response.status_code, status.HTTP_204_NO_CONTENT)


    def test_get_shows_the_correct_products_for_each_vendor( self) :
        response = self.client.get( reverse( "vendor-products", 
            args = ( self.vendor1.id, )))
        self.assertEqual( response.status_code, status.HTTP_200_OK)
        self.assertEqual( len( response.json()['data']), 4)

        response = self.client.get( reverse( "vendor-products", 
            args = ( self.vendor2.id, )))
        self.assertEqual( response.status_code, status.HTTP_200_OK)
        self.assertEqual( len( response.json()['data']), 2)


    def test_post_for_non_existent_vendor_returns_not_found( self) :
        response = self.client.post( reverse( "vendor-products", 
            args = ( 99999, )), {
            'product': {
                'name': "Product name",
                'code': 575757575757
            }
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_404_NOT_FOUND)


    def test_post_should_add_products_for_vendor( self) :
        response = self.client.post( reverse( "vendor-products", 
            args = ( self.vendor1.id, )), {
            'product': {
                'name': "Product name",
                'code': '575757575750'
            }
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_201_CREATED)
        self.assertEqual( Product.get_all_from_vendor( 
            self.vendor1.id).count(), 5)
        
        response = self.client.post( reverse( "vendor-products", 
            args = ( self.vendor3.id, )), {
            'product': {
                'name': "Product name",
                'code': '575757575750'
            }
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_201_CREATED)
        self.assertEqual( Product.get_all_from_vendor( 
            self.vendor3.id).count(), 1)
        

class ProductDetailsListAPITestCase( APITestCase, GenData) :

    def setUp( self) :
        self.client = APIClient()
        self.gen()
        

    def test_get_non_existent_product_yields_404( self) :
        response = self.client.get( reverse( "product-details", 
            args = ( 99999, )))
        self.assertEqual( response.status_code, status.HTTP_404_NOT_FOUND)
        

    def test_put_non_existent_product_yields_404( self) :
        response = self.client.put( reverse( "product-details", 
            args = ( 99999, )), {
            'product': {
                'name': "Product name"
            }
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_non_existent_product_yields_404( self) :
        response = self.client.delete( reverse( "product-details", 
            args = ( 99999, )))
        self.assertEqual( response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_get_works( self) :
        response = self.client.get( reverse( "product-details", 
            args = ( self.product10.id, )))
        self.assertEqual( response.status_code, status.HTTP_200_OK)
        self.assertEqual( response.json()['data']['name'], self.product10.name)
        self.assertEqual( response.json()['data']['code'], self.product10.code)
        self.assertEqual( response.json()['data']['price'], '0.00')


    def test_invalid_data_is_handled_correctly( self) :
        response = self.client.put( reverse( "product-details", 
            args = ( self.product10.id, )), {
            'product': {
                'price': -10.0
            }
        }, format = 'json')
        self.assertEqual( response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    
    def test_put_works( self) :
        response = self.client.put( reverse( "product-details", 
            args = ( self.product10.id, )), {
            'product': {
                'name': "Product name"
            }
        }, format = 'json')
        self.product10.refresh_from_db()
        self.assertEqual( response.status_code, status.HTTP_200_OK)
        self.assertEqual( ProductSerializer( self.product10).data, {
            'id': self.product10.id,
            'name': "Product name",
            'code': self.product10.code,
            'price': str( self.product10.price)
        })
        

    def test_delete_works( self) :
        response = self.client.delete( reverse( "product-details", 
            args = ( self.product10.id, )))
        self.assertEqual( response.status_code, status.HTTP_200_OK)
        response = self.client.delete( reverse( "product-details", 
            args = ( self.product10.id, )))
        self.assertEqual( response.status_code, status.HTTP_404_NOT_FOUND)
        