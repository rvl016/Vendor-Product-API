from django.db import models
from django.core.validators import *
from helpers.validation import validateRecord
from .validators import *
 
# Create your models here.
class Vendor( models.Model) :

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

  def validate( self) :
    return validateRecord( self)