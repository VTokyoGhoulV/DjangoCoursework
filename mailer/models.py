from django.db import models


# Create your models here.

class Recipient(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
