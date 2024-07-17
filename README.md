
# Task Management Project

This is a task management system developed with Django and Celery.

## Setup Instructions

### 1. Clone the Repository

```bash
mkdir task_management && cd task_management
git clone https://github.com/rushikesh-shinde-pyd/TaskManagement.git .
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies and Set Up

```bash
source setup.sh
```

### 4. Run the Development Server

```bash
python manage.py runserver
```

### 5. Run Celery Worker

```bash
celery -A task_management worker -B --loglevel=info
```

## API Documentation

You can access the API endpoints via Postman using the following collection:

[Postman Collection](https://documenter.getpostman.com/view/9822314/2sA3kRJPh9)

## Demo

You can watch a demo of the project here:

[Demo](https://drive.google.com/file/d/1ShcKWU5f5-Jr6MqcT-z1RT4VlWYamOOJ/view?usp=sharing)

## Screenshots

Here are some screenshots of the project:

![Screenshot 1](https://tinyurl.com/2yaqge7q)

![Screenshot 2](https://tinyurl.com/23pef4ng)
