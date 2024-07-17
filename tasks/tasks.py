# Standard library imports
import logging
import sys
from datetime import timedelta

# Django imports
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

# Third-party imports
from celery import shared_task
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

# Local imports
from .constants import SUBJECT_TASK_DUE
from .models import Task
from .utils import truncate_to_minute

logger = logging.getLogger(__name__)

@shared_task
def send_due_task_emails():
    """
    Sends email notifications for tasks due soon.

    Retrieves tasks due within 5 and 10 minutes from now and sends an email notification
    to the assigned user.

    """
    try:
        logger.info('Into send_due_task_emails')
        now = truncate_to_minute(timezone.now())
        five_minutes_later = now + timedelta(minutes=5)
        ten_minutes_later = now + timedelta(minutes=10)

        due_tasks = Task.objects.select_related('user').filter(
            due_date__in=[five_minutes_later, ten_minutes_later]
        )

        for task in due_tasks:
            plain_text_message = f"""
                Tasks Due Soon

                Title: {task.title}
                Due Date: {task.due_date}
                Status: {task.status}
            """

            html_message = render_to_string('tasks/due_tasks_email.html', {
                'task': task,
            })
            
            task.user.email_user(
                SUBJECT_TASK_DUE,
                plain_text_message,
                settings.EMAIL_HOST_USER,
                html_message=html_message,
                fail_silently=False,
            )

            logger.info(f"Email sent for task {task.id}")

    except Exception as e:
        _, __, tb = sys.exc_info()
        logger.error(f"Error in send_due_task_emails: {str(e)} at lineno: {tb.tb_lineno}")


@shared_task
def expired_tokens_cleanup():
    """
    Deletes expired tokens from the database.

    Finds tokens that have expired and deletes them from both `OutstandingToken` and `BlacklistedToken`.
    """
    try:
        logger.info('Into expired_tokens_cleanup')
        now = timezone.now()

        expired_tokens = OutstandingToken.objects.filter(expires_at__lt=now).iterator()

        for token in expired_tokens:
            BlacklistedToken.objects.create(token=token.token)
            token.delete()

    except Exception as e:
        _, __, tb = sys.exc_info()
        logger.error(f"Error in expired_tokens_cleanup: {str(e)} at lineno: {tb.tb_lineno}")