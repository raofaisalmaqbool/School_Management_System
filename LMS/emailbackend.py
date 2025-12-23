"""
Custom authentication backend for email-based login.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their email
    address instead of username.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user using email and password.
        
        Args:
            request: The HTTP request object
            username: Email address of the user
            password: Password of the user
            **kwargs: Additional keyword arguments
            
        Returns:
            User object if authentication succeeds, None otherwise
        """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None