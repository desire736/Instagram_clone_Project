from django.db import models
from django.contrib.auth.models import AbstractUser

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    avatar_image = models.ImageField(null=True, default='profile_img.jpg', blank=True)
    describtion = models.TextField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class CustomFollow(models.Model):
    '''Подписки, подписчики'''

    following = models.ForeignKey(
        CustomUser,
        blank=True,
        on_delete=models.CASCADE,
        related_name='following'
    )

    follower = models.ForeignKey(
        CustomUser,
        blank=True,
        on_delete=models.CASCADE,
        related_name='follower'
    )