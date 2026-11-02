from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from users.views import register, activate, UsersListView, UserBlockListView

urlpatterns = [
    path("register/", register, name="register"),
    path("activate/<int:pk>/<str:token>/", activate, name="activate"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_reset/", PasswordResetView.as_view(template_name="password_reset_form.html",
                                                      email_template_name="password_reset_email.txt",
                                                      subject_template_name="password_reset_subject.txt", ),
         name="password_reset"),

    path("password_reset_done/", PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name="password_reset_done"),

    path("password_reset_confirm/<str:uidb64>/<str:token>/",
         PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
         name="password_reset_confirm"),

    path("password_reset_complete/", PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name="password_reset_complete"),

    path("user_list", UsersListView.as_view(), name="user_list"),
    path("block_user/<int:pk>/", UserBlockListView.as_view(), name="block_user"),
]
