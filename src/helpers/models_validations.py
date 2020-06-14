from django.core.exceptions import ValidationError

# This class should be inherited by a Model class
class BasicValidator() :

    def validate_record( self) :
        try :
            self.full_clean()
            return {}
        except ValidationError as errors :
            return errors.message_dict
    
    @classmethod
    def id_exists( cls, id) :
        try :
            cls.objects.get( id = id)
            return True
        except :
            return False