from django.db import models
from django.core.validators import *
from djmoney.models.fields import MoneyField
from helpers.models_validations import BasicValidator
from .validators import *

# Create your models here.
class Product( models.Model, BasicValidator) :
    vendor = models.ForeignKey(
        'vendors.Vendor',
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

    code = models.IntegerField(
        validators = [
            RegexValidator( regex = CODE_REGEX, message = CODE_REGEX_MSG)
        ]
    )

    price = MoneyField( 
        null = True,
        default = None, 
        blank = True,
        max_digits = 14,
        decimal_places = 2,
        default_currency = 'USD'
    )
