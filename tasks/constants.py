STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]

SUBJECT_TASK_DUE = 'Task Due Soon'

NOT_AVAILABLE = 'Not available'

RESPONSE_500 = {'detail': 'Internal Server Error'}

CACHE_USER_KEY = 'user_details_{}'

CACHE_TASK_KEY = 'task_list_{}'
