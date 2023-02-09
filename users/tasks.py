import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


@shared_task
def send_email_verification(user_id):
    """The task is to send a confirmation email to the user's email address."""
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)  # link valid for 48 hours
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    # Made an record in the database. uuid.uuid4() - will create a unique code.
    record.send_verification_email()  # Sent an email

