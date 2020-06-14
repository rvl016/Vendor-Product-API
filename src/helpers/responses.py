from django.http import JsonResponse

class Responses :

    @staticmethod
    def _reply_not_found() :
        return JsonResponse( {
            'error': "The requested content does not exist."
        }, status = 204)

    @staticmethod
    def _reply_created_or_failed( errors) :
        if errors == {} :
            return JsonResponse( {
                'message': "Successfully created!"
            }, status = 201)
        return Responses._reply_not_acceptable( errors)

    @staticmethod
    def _reply_updated_or_failed( errors) :
        if errors == {} :
            return JsonResponse( {
                'message': "Successfully updated!"
            }, status = 200)
        return Responses._reply_not_acceptable( errors)

    @staticmethod
    def _reply_get_ok( data) :
        return JsonResponse( {
            'message': "I shall serve you, Sir!",
            'data': data
        }, status = 200)

    @staticmethod
    def _reply_ok() :
        return JsonResponse( {
            'message': "Your request was successfully done!"
        }, status = 200)

    @staticmethod
    def _reply_bad_request() :
        return JsonResponse( {
            'message': "Your data could not be read or had invalid keys."
        }, status = 400)

    @staticmethod
    def _reply_not_acceptable( errors) :
        return JsonResponse( {
            'message': "Your request did not pass in our validation.",
            'errors': errors
        }, status = 406)