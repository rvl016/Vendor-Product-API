from django.test import TestCase
from ..models import Vendor

class VendorTestCase( TestCase) :

  def setUp( self) :
    self.noneVendor = Vendor()
    self.underMinLenName = Vendor( name = "Hi")
    self.noCityVendor = Vendor( name = "MyCompany", 
      cnpj = "55.555.555/0000-00")
    self.correctVendor = Vendor( name = "Bradoo", cnpj = "26.402.093/0001-74", 
      city = "São Paulo")

  def test_vendorIsProtectedByRequiredFields( self) :
    errors = self.noneVendor.validate()
    self.assertEqual( list( errors.keys()), ['name', 'cnpj'])

  def test_vendorNameShouldBeAtLeastLong( self) :
    errors = self.underMinLenName.validate()
    self.assertNotEqual( errors.get( 'name'), None)

  def test_vendorDoesNotRequireCity( self) :
    errors = self.noCityVendor.validate()
    self.assertEqual( errors, {})

  def test_validRecordIsAllowed( self) :
    errors = self.correctVendor.validate()
    self.assertEqual( errors, {})


