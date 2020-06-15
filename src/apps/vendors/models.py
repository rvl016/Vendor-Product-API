from django.db import models

from django.core.validators import *
from helpers.models_validations import BasicValidator

from .validators import *
 
# Create your models here.
class Vendor( models.Model, BasicValidator) :

    name = models.CharField(
        max_length = NAME_MAX_LEN,
        validators = [
            MaxLengthValidator( NAME_MAX_LEN, message = NAME_MAX_LEN_MSG),
            MinLengthValidator( NAME_MIN_LEN, message = NAME_MIN_LEN_MSG),
            ProhibitNullCharactersValidator( message = NAME_NULL_CHAR_MSG)
        ]
    ) 

    cnpj = models.CharField(
        max_length = 18,
        unique = True,
        validators = [
            RegexValidator( regex = CNPJ_REGEX, message = CNPJ_REGEX_MSG)
        ]
    )

    city = models.CharField(
        max_length = CITY_MAX_LEN,
        default = "Unknown",
        validators = [
            MaxLengthValidator( NAME_MAX_LEN, message = NAME_MAX_LEN_MSG),
            MinLengthValidator( NAME_MIN_LEN, message = NAME_MIN_LEN_MSG),
            ProhibitNullCharactersValidator( message = NAME_NULL_CHAR_MSG)
        ]
    )  

    fields = {'name', 'cnpj', 'city'}

    def __str__( self) :
        return self.name

    @classmethod
    def get_all( cls) :
        return cls.objects.all()

    @classmethod
    def get( cls, id) :
        return cls.objects.get( id = id)

    @classmethod
    def destroy( cls, id_list) :
        cls.objects.filter( id__in = id_list).delete()

    @classmethod 
    def create( cls, data_dict) :
        vendor = cls( **data_dict)
        return vendor.__show_errors_or_save()

    @classmethod
    def find_and_try_to_update_with( cls, id, data) :
        vendor = cls.get( id)
        return vendor.update_record_with( data)

    def update_record_with( self, data) :
        self.__update_fields( data)
        return self.__show_errors_or_save()

    # private
    def __update_fields( self, data) :
        self.name = data.get( 'name') or self.name
        self.cnpj = data.get( 'cnpj') or self.cnpj
        self.city = data.get( 'city') or self.city

    # private
    def __show_errors_or_save( self) :
        errors = self.validate_record()
        if errors == {} :
            self.save()
        return errors