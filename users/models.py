from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail


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
        send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            [self.user.email],
            fail_silently=False,
        )

    class Meta:
        verbose_name = 'Подтверждение почты'
        verbose_name_plural = 'Подтверждение почты'
