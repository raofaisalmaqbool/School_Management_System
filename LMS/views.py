"""
DEPRECATED: This file is no longer used.
All views have been moved to the LMS/views/ package.

Please import views from:
- LMS.views.auth_views
- LMS.views.principal_views
- LMS.views.teacher_views
- LMS.views.student_views
"""

# Import all views from the new structure for backward compatibility
from .views.auth_views import *
from .views.principal_views import *
from .views.teacher_views import *
from .views.student_views import *
