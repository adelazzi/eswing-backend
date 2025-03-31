from rest_framework.response import Response
from rest_framework import status

def create_response(data=None, message="", errors=None, status_code=status.HTTP_200_OK):
    """
    Creates a standardized response format for all API endpoints.
    
    Args:
        data: The data to be returned in the response
        message: A message describing the response
        errors: Any errors that occurred
        status_code: The HTTP status code
        
    Returns:
        Response object with standardized format
    """
    response_data = {
        "status": "success" if status_code < 400 else "error",
        "message": message,
        "data": data
    }
    
    if errors:
        response_data["errors"] = errors
    
    return Response(response_data, status=status_code)
