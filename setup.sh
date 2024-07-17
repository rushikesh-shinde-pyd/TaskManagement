#!/bin/bash

set -e

# Update package list
echo "Updating package list..."
sudo apt update

# Install Redis server
echo "Installing Redis server..."
sudo apt install -y redis-server

# Start and enable Redis service
echo "Starting and enabling Redis service..."
sudo systemctl start redis-server

# Check Redis service status
echo "Checking Redis service status..."
sudo systemctl status redis-server

echo "Redis installation and setup completed."

# Set up Python virtual environment and activate it
echo "Setting up Python virtual environment..."
python3 -m venv .venv

# Delete existing migrations
# echo "Deleting existing migrations..."
# rm db.sqlite3 tasks/migrations/00*

# Create log folder
echo "log folder creating..."
mkdir log

echo "Activating virtual environment..."
. .venv/bin/activate

# Install required Python packages
echo "Installing required Python packages..."
pip install -r requirements.txt

# Run Django migrations and start the server
echo "Running Django migrations..."
python manage.py makemigrations

echo "Applying Django migrations..."
python manage.py migrate

echo "Project setup completed."

echo "Starting Django development server..."
python manage.py runserver