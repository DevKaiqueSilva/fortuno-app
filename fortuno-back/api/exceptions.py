from rest_framework.views import exception_handler
from rest_framework.response import Response
import traceback

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': str(exc),
            'details': response.data
        }
        
        # Add traceback in debug mode
        from django.conf import settings
        if settings.DEBUG:
            custom_response_data['traceback'] = traceback.format_exc()
            
        response.data = custom_response_data
    
    return response