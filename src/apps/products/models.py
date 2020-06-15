from decimal import Decimal
from django.db import models, transaction, IntegrityError

from apps.vendors.models import Vendor

from django.core.validators import *
from helpers.models_validations import BasicValidator

from .validators import *

# Create your models here.
class Product( models.Model, BasicValidator) :

    vendor = models.ForeignKey(
        Vendor,
        on_delete = models.CASCADE
    )

    name = models.CharField(
        max_length = NAME_MAX_LEN,
        validators = [
            MaxLengthValidator( NAME_MAX_LEN, message = NAME_MAX_LEN_MSG),
            MinLengthValidator( NAME_MIN_LEN, message = NAME_MIN_LEN_MSG),
            ProhibitNullCharactersValidator( message = NAME_NULL_CHAR_MSG)
        ]
    )

    code = models.CharField(
        max_length = CODE_LEN,
        validators = [
            RegexValidator( regex = CODE_REGEX, message = CODE_REGEX_MSG)
        ]
    )

    price = models.DecimalField( 
        null = True,
        blank = True,
        default = None,
        max_digits = 14,
        decimal_places = 2,
        validators = [
            MinValueValidator( Decimal( 0).quantize( Decimal( '.01')), 
                message = PRICE_POSITIVE_MSG)
        ]
    )

    fields = {'vendor', 'name', 'code', 'price'}

    def __str__( self) :
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint( fields = ['vendor', 'code'], 
                name = 'unique products for each vendor')
        ]

    @classmethod
    def get_all( cls) :
        return cls.objects.all()

    @classmethod
    def get_all_from_vendor( cls, vendor_id) :
        return cls.objects.filter( vendor__id = vendor_id).select_related()

    @classmethod
    def get_by_id( cls, id) :
        return cls.objects.get( id = id)

    @classmethod
    def get_by_code( cls, code) :
        return cls.objects.filter( code = code).select_related()

    @classmethod
    def destroy( cls, id_list) :
        cls.objects.filter( id__in = id_list).delete()

    @classmethod 
    def create( cls, data_dict, vendor_id) :
        vendor = Vendor.get( vendor_id)
        return cls.create_with_instance( data_dict, vendor)

    @classmethod 
    def create_multiple( cls, data_array, vendor_id) :
        vendor = Vendor.get( vendor_id)
        try :
            with transaction.atomic() :
                errors = cls.transact_create_multiple( data_array, vendor)
        except IntegrityError as error :
            return error.args[0]
        return errors

    @classmethod
    def transact_create_multiple( cls, data_array, vendor) :
        errors = { 'products': [] }
        errors['products'] = cls.create_multiple_with_vendor_instance( 
            data_array, vendor)
        if any( [error != {} for error in errors['products']]) :
            raise IntegrityError( errors)
        return {}
        
    # should be in an atomic transaction
    @classmethod
    def create_multiple_with_vendor_instance( cls, data_array, vendor) :
        errors = list( map( lambda product: 
            Product.create_with_instance( product, vendor), data_array))
        return errors
        
    @classmethod
    def create_with_instance( cls, data_dict, vendor) :
        data_dict['price'] = Product.decimize_it( data_dict.get( 'price'))
        product = cls( **data_dict, vendor = vendor)
        return product.__show_errors_or_save()
        
    @classmethod
    def find_and_try_to_update_with( cls, id, data) :
        product = cls.get_by_id( id)
        return product.update_record_with( data)

    def update_record_with( self, data) :
        self.__update_fields( data)
        return self.__show_errors_or_save()

    # private
    def __update_fields( self, data) :
        self.name = data.get( 'name') or self.name
        self.code = data.get( 'code') or self.code
        self.price = data.get( 'price') or self.price
        self.price = Product.decimize_it( self.price)

    # private
    def __show_errors_or_save( self) :
        errors = self.validate_record()
        if errors == {} :
            self.save()
        return errors

    @staticmethod
    def decimize_it( number) :
        if number == None :
            return None
        return Decimal( number).quantize( Decimal( '.01'))