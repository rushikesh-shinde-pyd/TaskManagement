mkdir task_management && cd task_management
git clone https://github.com/rushikesh-shinde-pyd/TaskManagement.git .
. setup.sh
celery -A task_management worker -B --loglevel=info
Postman collection - https://documenter.getpostman.com/view/9822314/2sA3kRJPh9