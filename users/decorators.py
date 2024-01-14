from rest_framework.response import Response
from rest_framework import status

def buyer_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.user_type == 1:
            return Response({'error': 'You must be a buyer to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        return function(request, *args, **kwargs)
    return wrapper


def seller_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.user_type == 2:
            return Response({'error': 'You must be a seller to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        return function(request, *args, **kwargs)
    return wrapper


def admin_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.user_type == 3:
            return Response({'error': 'You must be an admin to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        return function(request, *args, **kwargs)
    return wrapper