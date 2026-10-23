from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailer.models import Mailer, MailerAttempt


def send_mailing(mailer_id):
    mailer = Mailer.objects.get(id=mailer_id)
    current_time = timezone.now()

    if mailer.start_time > current_time:
        raise ValueError("Время рассылки еще не наступило, отправка сообщений не возможна")

    if mailer.end_time <= current_time:
        raise ValueError("Рассылка окончена, отправка сообщений не возможна")

    letter = mailer.message

    for person in mailer.recipient.all():
        try:
            result = send_mail(
                subject=letter.topic,
                message=letter.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[person.email],
                fail_silently=False,
            )

        except Exception as error:
            MailerAttempt.objects.create(mailer=mailer, recipient=person, status="Не успешно", error_message=str(error))

        else:
            if result == 1:
                MailerAttempt.objects.create(mailer=mailer, recipient=person, status="Успешно")
            else:
                MailerAttempt.objects.create(mailer=mailer, recipient=person, status="Не успешно",
                                             error_message="Функция отправки вернула 0")
