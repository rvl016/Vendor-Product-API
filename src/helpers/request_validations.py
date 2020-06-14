
class RequestValidator : 

    @staticmethod
    def _is_data_valid_for( request_data, fields) :
        if request_data == None :
            return False
        return set( request_data.keys()).issubset( fields)

    @staticmethod
    def _is_data_an_array_of_ids( request_data) :
        if not isinstance( request_data, list) :
            return False
        return all( [isinstance( element, int) for element in request_data])