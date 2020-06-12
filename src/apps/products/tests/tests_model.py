from django.test import TestCase
from ..models import Product
from apps.vendors.models import Vendor

from djmoney.money import Money

class ProductTestCase( TestCase) :

  def setUp( self) :
    self.correctVendor = Vendor.objects.create( name = "Bradoo", 
      cnpj = "26.402.093/0001-74", city = "São Paulo")
    self.correctVendor.save()
    self.orange = Product( name = "Orange", code = 123454589012)

  def test_correctProductWithNoPriceIsValid( self) :
    self.apple = Product( vendor = self.correctVendor, name = "Apple", 
      code = 123456789012)
    errors = self.apple.validate()
    self.assertEqual( errors, {})
    self.apple.save()
    
  def test_correctProductWithPriceIsValid( self) :
    self.apple = Product( vendor = self.correctVendor, name = "Apple", 
      code = 123456789012, price = Money( 1.24))
    errors = self.apple.validate()
    self.assertEqual( errors, {})
    self.apple.save()

  def test_productIsDependentOnVendor( self) :
    errors = self.orange.validate()
    self.assertEqual( list( errors.keys()), ['vendor'])

  def test_assertProductWithNoPriceIsNull( self) :
    self.test_correctProductWithNoPriceIsValid()
    self.assertIsNone( self.apple.price)

  def test_destroyingVendorLeadsToItsProductsDestruction( self) :
    self.test_correctProductWithPriceIsValid()
    self.correctVendor.delete()
    self.assertRaises( Product.DoesNotExist, Product.objects.get, 
      code = 123456789012)
