from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    """
    Use the existing User model (AbstractUser) so as not to create all the fields again.
    Added custom email confirmation field.
    """
    image = models.ImageField(upload_to='users_images', null=True, blank=True, default=None)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    """Mail confirmation model"""
    code = models.UUIDField(unique=True)  # a unique link with a code is generated for each user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()  # link end date

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        """Method of sending email with mail confirmation"""
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Account verification for {self.user.username}'
        message = 'To verify an account for {} follow this link: {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        """Method for checking the expiration date of a link"""
        return True if now() >= self.expiration else False

    class Meta:
        verbose_name = 'Подтверждение почты'
        verbose_name_plural = 'Подтверждение почты'
