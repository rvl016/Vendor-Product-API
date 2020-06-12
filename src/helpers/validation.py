from django.core.exceptions import ValidationError

def validateRecord( object) :
  try :
    object.full_clean()
    return {}
  except ValidationError as errors :
    return errors.message_dict