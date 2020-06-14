from django.test import TestCase
from ..models import Vendor

class VendorModelTestCase( TestCase) :
    
    def setUp( self) :
        self.none_vendor = Vendor()
        self.under_min_len_name = Vendor( name = "Hi")
        self.no_city_vendor = Vendor( name = "MyCompany", 
            cnpj = "55.555.555/0000-00")
        self.correct_vendor = Vendor( name = "Bradoo", 
            cnpj = "26.402.093/0001-74", city = "São Paulo")

    def test_vendor_is_protected_by_required_fields( self) :
        errors = self.none_vendor.validate_record()
        self.assertEqual( list( errors.keys()), ['name', 'cnpj'])

    def test_vendor_name_should_be_at_least_long( self) :
        errors = self.under_min_len_name.validate_record()
        self.assertNotEqual( errors.get( 'name'), None)

    def test_vendor_does_not_require_city( self) :
        errors = self.no_city_vendor.validate_record()
        self.assertEqual( errors, {})

    def test_valid_record_is_allowed( self) :
        errors = self.correct_vendor.validate_record()
        self.assertEqual( errors, {})

    def test_get_method_works( self) :
        self.save_vendors()
        self.correct_vendor.refresh_from_db()
        self.assertRaises( Vendor.DoesNotExist, Vendor.get, 9999)
        self.assertEqual( Vendor.get( self.correct_vendor.id).id, 
            self.correct_vendor.id)

    def test_create_method_works( self) :
        vendor = {
            'name': "Ravi Inc.",
            'cnpj': "42.424.242/4242-42"
        }
        self.assertEqual( Vendor.create( vendor), {})

    def save_vendors( self) :
        self.no_city_vendor.save()
        self.correct_vendor.save()
