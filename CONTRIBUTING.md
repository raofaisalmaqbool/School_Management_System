# Contributing to School Management System

Thank you for your interest in contributing to the School Management System! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Detailed steps to reproduce the bug
- Expected behavior vs actual behavior
- Screenshots if applicable
- Your environment (OS, Python version, Django version)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- A clear description of the enhancement
- Why this enhancement would be useful
- Any implementation details you've considered

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow the code style**
   - Follow PEP 8 guidelines
   - Add docstrings to all functions and classes
   - Keep functions focused and single-purpose
   - Use meaningful variable names

3. **Write tests** for new features
   ```bash
   python manage.py test
   ```

4. **Update documentation** if needed
   - Update README.md for user-facing changes
   - Add docstrings for new code
   - Update inline comments

5. **Commit your changes**
   ```bash
   git commit -m "feat: add new feature description"
   ```
   
   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `style:` for formatting changes
   - `refactor:` for code refactoring
   - `test:` for adding tests
   - `chore:` for maintenance tasks

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all tests pass
   - Wait for review

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/School_Management_System.git
   cd School_Management_System
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Code Style Guidelines

### Python Code Style

- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use double quotes for strings
- Add type hints where appropriate

### Django Best Practices

- Use class-based views where appropriate
- Keep views thin, business logic in models or services
- Use Django's built-in authentication
- Always use Django's ORM (avoid raw SQL)
- Use Django's form validation
- Add proper error handling with try-except blocks
- Log errors appropriately

### Documentation

- Add docstrings to all functions and classes
- Use Google-style docstrings format
- Document all parameters and return values
- Include usage examples for complex functions

Example:
```python
def calculate_total_marks(assignment: int, presentation: int, exam: int) -> int:
    """
    Calculate total marks from assignment, presentation, and exam scores.
    
    Args:
        assignment: Assignment marks (0-100)
        presentation: Presentation marks (0-100)
        exam: Exam marks (0-100)
        
    Returns:
        Total marks sum
        
    Example:
        >>> calculate_total_marks(85, 90, 88)
        263
    """
    return assignment + presentation + exam
```

### Testing

- Write unit tests for all new features
- Maintain test coverage above 80%
- Test both success and failure cases
- Use Django's TestCase class
- Mock external dependencies

Example:
```python
from django.test import TestCase
from LMS.models import Student

class StudentTestCase(TestCase):
    def setUp(self):
        # Set up test data
        pass
    
    def test_student_creation(self):
        # Test student creation logic
        pass
```

## Project Structure

When adding new features, follow this structure:

```
LMS/
├── models.py           # Database models
├── views/              # View modules (organized by user type)
├── forms.py            # Django forms
├── utils.py            # Utility functions
├── admin.py            # Admin configuration
├── urls.py             # URL routing (if app-specific)
└── tests/              # Test modules
    ├── test_models.py
    ├── test_views.py
    └── test_forms.py
```

## Areas Needing Contribution

We especially welcome contributions in these areas:

### High Priority
- [ ] Unit tests for all views
- [ ] Integration tests
- [ ] API documentation
- [ ] Email notification system
- [ ] SMS notification integration
- [ ] Export functionality (PDF/Excel)

### Medium Priority
- [ ] Student result management improvements
- [ ] Timetable management
- [ ] Fee management system
- [ ] Library management
- [ ] Parent portal

### Low Priority
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Dark mode for UI

## Questions?

Feel free to create an issue with the "question" label if you need help or clarification.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to School Management System!
