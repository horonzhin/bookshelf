import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    # время дейтвия ссылки закончится через 48 часов
    expiration = now() + timedelta(hours=48)
    # uuid.uuid4() - создаст уникальный код.
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()

