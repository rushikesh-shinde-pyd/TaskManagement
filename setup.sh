#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt update

# Install Redis server
echo "Installing Redis server..."
sudo apt install -y redis-server

# Start and enable Redis service
echo "Starting and enabling Redis service..."
sudo systemctl start redis-server
# sudo systemctl enable redis-server # Uncomment if you want Redis to start on boot

echo "Redis installation and setup completed."

# Create log folder
echo "Creating log folder..."
mkdir log

# Install required Python packages
echo "Installing required Python packages..."
pip install -r requirements.txt

# Run Django migrations and start the server
echo "Running Django migrations..."
python manage.py makemigrations

echo "Applying Django migrations..."
python manage.py migrate

echo "Project setup completed."
echo -e "\n"
echo "Run - 'python manage.py runserver' to start the development server."
echo "Run - 'celery -A task_management worker -B --loglevel=info' to start a Celery worker along with the Celery beat scheduler."