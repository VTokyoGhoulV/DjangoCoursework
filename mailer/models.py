from django.utils import timezone

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


class Message(models.Model):
    topic = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailer(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=255, default="Создана")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipient = models.ManyToManyField(Recipient)

    def update_status(self):

        actual_time = timezone.now()
        if actual_time < self.start_time:
            self.status = "Создана"
        elif self.start_time <= actual_time < self.end_time:
            self.status = "Запущена"
        elif actual_time > self.end_time:
            self.status = "Завершена"

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class MailerAttempt(models.Model):
    mailing = models.ForeignKey(Mailer, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20)
    server_response = models.TextField(blank=True)