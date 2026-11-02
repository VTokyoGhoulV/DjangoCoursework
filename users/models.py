from django.conf import settings
from django.db import models

# Create your models here.

class UserBlock(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_block'
        permissions = [("block_user", "Может блокировать пользователя")]
