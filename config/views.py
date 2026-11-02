from django.contrib.messages import get_messages
from django.core.cache import cache
from django.shortcuts import render
from django.utils import timezone
from django.utils.cache import (
    add_never_cache_headers,
    patch_cache_control,
    patch_vary_headers,
)

from mailer.models import Mailer, Recipient


def home(request):
    mailer_count = cache.get('home_total_mailings')

    if mailer_count is None:
        mailer_count = Mailer.objects.count()
        cache.set('home_total_mailings', mailer_count, 60)

    recipient_count = cache.get('home_total_recipients')

    if recipient_count is None:
        recipient_count = Recipient.objects.count()
        cache.set('home_total_recipients', recipient_count, 60)

    current_time = timezone.now()

    active_mailers = cache.get('home_active_mailers')
    if active_mailers is None:

        active_mailers = 0

        for mailer in Mailer.objects.filter(start_time__lte=current_time, end_time__gt=current_time):
            mailer.update_status()
            if mailer.status == "Запущена":
                active_mailers += 1

        cache.set('home_active_mailers', active_mailers, 60)

    has_messages = bool(get_messages(request))
    response = render(request, 'home.html', {
        'total_mailings': mailer_count,
        'total_recipients': recipient_count,
        'active_mailers': active_mailers,
    })

    if has_messages or request.user.is_authenticated:
        add_never_cache_headers(response)
    else:
        patch_cache_control(response, private=True, max_age=30)

    patch_vary_headers(response, ["Cookie"])
    return response
