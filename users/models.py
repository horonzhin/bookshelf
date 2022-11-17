from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now


# для того чтобы расширить имеющуюся модель user, а не создавать все поля заново, наследуемся от AbstractUser
class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True, default=None)
    # проверка на подтверждение почты user
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    # для каждого user генерируется уникальная ссылка с кодом
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    # срок окончания действия ссылки
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    # метод отправки email с подтверждением почты
    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email='from@example.com',
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    # метод для проверки срока годности ссылки
    def is_expired(self):
        return True if now() >= self.expiration else False

    class Meta:
        verbose_name = 'Подтверждение почты'
        verbose_name_plural = 'Подтверждение почты'
