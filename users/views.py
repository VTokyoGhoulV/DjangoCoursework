from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from config import settings
from users.forms import RegisterForm
from users.models import UserBlock


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            token = default_token_generator.make_token(user)
            activate_path = reverse("activate", kwargs={"pk": user.pk, "token": token})
            activate_url = request.build_absolute_uri(activate_path)

            try:
                result = send_mail(subject="Подтверждение регистрации", message=activate_url,
                                   from_email=settings.DEFAULT_FROM_EMAIL,
                                   recipient_list=[user.email])

            except Exception:
                user.delete()
                form.add_error(None, "Не удалось отправить сообщение для подтверждения, попробуйте позже")

            else:
                if result:
                    messages.success(request, "Вам было отправлено сообщение на почту для подтверждения аккаунта")
                    return redirect("index")
                else:
                    user.delete()
                    form.add_error(None, "Не удалось отправить сообщение для подтверждения, попробуйте позже")

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def activate(request, pk, token):
    user = get_object_or_404(User, pk=pk)

    if UserBlock.objects.filter(user=user).exists():
        messages.error(request, "Учетная запись заблокирована менеджером")
        return redirect("index")

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        messages.success(request, "Успешная регистрация")

    else:
        messages.error(request, "Ссылка подтверждения недействительна")
    return redirect("index")


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = get_user_model()
    permission_required = 'auth.view_user'
    template_name = 'user_list.html'
    context_object_name = 'service_users'


class UserBlockListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'users.block_user'

    def post(self, request, pk):
        account = get_object_or_404(get_user_model(), pk=pk)

        if account.pk == request.user.pk or account.is_superuser:
            raise PermissionDenied("Не возможно заблокировать себя или супер-пользователя")

        with transaction.atomic():
            UserBlock.objects.get_or_create(user=account)
            account.is_active = False
            account.save(update_fields=["is_active"])

        return redirect("user_list")
