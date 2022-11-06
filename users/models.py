from django.db import models
from django.contrib.auth.models import AbstractUser


# для того чтобы расширить имеющуюся модель user, а не создавать все поля заново, наследуемся от AbstractUser
class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True, default=None)
