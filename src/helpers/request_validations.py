
class RequestValidator : 

    @staticmethod
    def _is_data_valid_for( request_data, fields) :
        return request_data != None and set( 
            request_data.keys()).issubset( fields)

    @staticmethod
    def _is_data_an_array_of_ids( request_data) :
        return isinstance( request_data, list) and all( 
            [isinstance( element, int) for element in request_data])

    @staticmethod
    def _is_data_an_array_with_fields( request_data, fields) :
        return isinstance( request_data, list) and all(
            [RequestValidator._is_data_valid_for( data, fields) 
            for data in request_data])
