from django.urls import path

from mailer import views

urlpatterns = [
    path("create_recipient/", views.RecipientCreateView.as_view(), name="create_recipient"),
    path("list_recipients/", views.RecipientListView.as_view(), name="list_recipients"),
    path("detail_recipient/<int:pk>/", views.RecipientDetailView.as_view(), name="detail_recipient"),
    path("update_recipient/<int:pk>/", views.RecipientUpdateView.as_view(), name="update_recipient"),
    path("delete_recipient/<int:pk>/", views.RecipientDeleteView.as_view(), name="delete_recipient"),
]
