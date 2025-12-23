"""
Utility functions for validation and helper methods.
"""
import re
from typing import Dict, Optional


class FormValidator:
    """
    Class containing form validation methods.
    """
    
    @staticmethod
    def validate_name(name: str, field_name: str = "Name") -> Optional[str]:
        """
        Validate that a name contains only alphabetic characters.
        
        Args:
            name: The name to validate
            field_name: Name of the field for error messages
            
        Returns:
            Error message if validation fails, None otherwise
        """
        if not name or not name.strip():
            return f"Please enter {field_name.lower()}."
        
        if not name.replace(" ", "").isalpha():
            return f"Please enter a valid {field_name.lower()} (letters only)."
        
        return None
    
    @staticmethod
    def validate_email(email: str) -> Optional[str]:
        """
        Validate email format.
        
        Args:
            email: The email to validate
            
        Returns:
            Error message if validation fails, None otherwise
        """
        if not email or not email.strip():
            return "Please enter an email address."
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return "Please enter a valid email address."
        
        return None
    
    @staticmethod
    def validate_username(username: str) -> Optional[str]:
        """
        Validate username format (alphanumeric only).
        
        Args:
            username: The username to validate
            
        Returns:
            Error message if validation fails, None otherwise
        """
        if not username or not username.strip():
            return "Please enter a username."
        
        if not username.isalnum():
            return "Username must contain only letters and numbers."
        
        if len(username) < 3:
            return "Username must be at least 3 characters long."
        
        return None
    
    @staticmethod
    def validate_password(password: str) -> Optional[str]:
        """
        Validate password strength.
        
        Args:
            password: The password to validate
            
        Returns:
            Error message if validation fails, None otherwise
        """
        if not password:
            return "Please enter a password."
        
        if len(password) < 6:
            return "Password must be at least 6 characters long."
        
        return None
    
    @staticmethod
    def validate_image(image_file) -> Optional[str]:
        """
        Validate image file type.
        
        Args:
            image_file: The uploaded image file
            
        Returns:
            Error message if validation fails, None otherwise
        """
        if not image_file:
            return None  # Image is optional
        
        allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif']
        file_name = str(image_file)
        
        if not any(file_name.lower().endswith(ext) for ext in allowed_extensions):
            return "Please upload a valid image file (PNG, JPG, or JPEG)."
        
        return None
    
    @staticmethod
    def validate_required_fields(data: Dict[str, any], required_fields: list) -> Optional[str]:
        """
        Check if all required fields are provided.
        
        Args:
            data: Dictionary of form data
            required_fields: List of required field names
            
        Returns:
            Error message if validation fails, None otherwise
        """
        missing_fields = []
        
        for field in required_fields:
            value = data.get(field)
            if not value or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field.replace('_', ' ').title())
        
        if missing_fields:
            return f"Please fill in the following required fields: {', '.join(missing_fields)}"
        
        return None


def get_status_display(status: int) -> str:
    """
    Convert status code to display text.
    
    Args:
        status: Status code (0=Pending, 1=Approved, 2=Rejected)
        
    Returns:
        Display text for the status
    """
    status_map = {
        0: 'Pending',
        1: 'Approved',
        2: 'Rejected'
    }
    return status_map.get(status, 'Unknown')


def get_user_type_display(user_type: str) -> str:
    """
    Convert user type code to display text.
    
    Args:
        user_type: User type code ('1', '2', '3')
        
    Returns:
        Display text for the user type
    """
    type_map = {
        '1': 'Principal',
        '2': 'Teacher',
        '3': 'Student'
    }
    return type_map.get(user_type, 'Unknown')
