from django.shortcuts import render
from django.utils import timezone

from mailer.models import Mailer, Recipient


def home(request):
    mailer_count = Mailer.objects.count()
    recipient_count = Recipient.objects.count()
    current_time = timezone.now()

    active_mailers = 0
    for mailer in Mailer.objects.filter(start_time__lte=current_time, end_time__gt=current_time):
        mailer.update_status()
        if mailer.status == "Запущена":
            active_mailers += 1

    return render(request, 'home.html', {
        'total_mailings': mailer_count,
        'total_recipients': recipient_count,
        'active_mailers': active_mailers,
    })
