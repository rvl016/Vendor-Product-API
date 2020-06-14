from django.test import TestCase
from ..models import Product
from apps.vendors.models import Vendor

from djmoney.money import Money

class ProductTestCase( TestCase) :
    def setUp( self) :
        self.correct_vendor = Vendor.objects.create( name = "Bradoo", 
        cnpj = "26.402.093/0001-74", city = "São Paulo")
        self.correct_vendor.save()
        self.orange = Product( name = "Orange", code = 123454589012)

    def test_correct_product_with_no_price_is_valid( self) :
        self.apple = Product( vendor = self.correct_vendor, name = "Apple", 
        code = 123456789012)
        errors = self.apple.validate_record()
        self.assertEqual( errors, {})
        self.apple.save()
        
    def test_correct_product_with_price_is_valid( self) :
        self.apple = Product( vendor = self.correct_vendor, name = "Apple", 
        code = 123456789012, price = Money( 1.24))
        errors = self.apple.validate_record()
        self.assertEqual( errors, {})
        self.apple.save()

    def test_product_is_dependent_on_vendor( self) :
        errors = self.orange.validate_record()
        self.assertEqual( list( errors.keys()), ['vendor'])

    def test_assert_product_with_no_price_is_null( self) :
        self.test_correct_product_with_no_price_is_valid()
        self.assertIsNone( self.apple.price)

    def test_destroying_vendor_leads_to_its_products_destruction( self) :
        self.test_correct_product_with_price_is_valid()
        self.correct_vendor.delete()
        self.assertRaises( Product.DoesNotExist, Product.objects.get, 
        code = 123456789012)
