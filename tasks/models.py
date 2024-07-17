# Django imports
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Local imports
from .constants import STATUS_CHOICES, NOT_AVAILABLE

User = get_user_model()


class BaseModel(models.Model):
    """
    Base model for common fields like creation and update timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True, help_text='The date and time when this object was created.')
    updated_at = models.DateTimeField(auto_now=True, help_text='The date and time when this object was last updated.')

    class Meta:
        abstract = True


class Task(BaseModel):   
    """
    Represents a task associated with a user.
    """
    user        = models.ForeignKey(User, on_delete=models.CASCADE, help_text='The user who owns this task.')
    title       = models.CharField(max_length=128, default=NOT_AVAILABLE, help_text='The title of the task.')
    description = models.TextField(max_length=256, default=NOT_AVAILABLE, help_text='Detailed description of the task.')
    status      = models.CharField(max_length=16, choices=STATUS_CHOICES, default='draft', help_text='Current status of the task.')
    due_date    = models.DateTimeField(default=timezone.now, help_text='The due date and time for completing this task.')

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]