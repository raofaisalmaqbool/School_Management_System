#!/bin/bash

# School Management System Setup Script
# This script helps you set up the project quickly

echo "=========================================="
echo "School Management System Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 is installed"

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "  Version: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate 2>/dev/null
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "⚠️  Please edit .env file with your configuration"
else
    echo "⚠️  .env file already exists. Skipping..."
fi
echo ""

# Create media directory
echo "Creating media directory..."
mkdir -p media/profile_pics
echo "✓ Media directory created"
echo ""

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate
if [ $? -eq 0 ]; then
    echo "✓ Migrations completed successfully"
else
    echo "❌ Migration failed"
    exit 1
fi
echo ""

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
echo "✓ Static files collected"
echo ""

# Ask to create superuser
echo "=========================================="
echo "Would you like to create a superuser now? (y/n)"
read -r CREATE_SUPERUSER

if [ "$CREATE_SUPERUSER" = "y" ] || [ "$CREATE_SUPERUSER" = "Y" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser
else
    echo "⚠️  You can create a superuser later using: python manage.py createsuperuser"
fi
echo ""

# Final message
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. If using MySQL, create the database first"
echo "3. Run the development server:"
echo "   python manage.py runserver"
echo ""
echo "Access the application at: http://localhost:8000"
echo "Admin panel: http://localhost:8000/admin"
echo ""
echo "For more information, see README.md"
echo "=========================================="
