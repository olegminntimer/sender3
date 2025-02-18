from django.urls import path

from send.apps import SendConfig
from send.views import RecipientCreateView, RecipientListView, main_view, RecipientUpdateView, RecipientDetailView, \
    RecipientDeleteView

app_name = SendConfig.name

urlpatterns = [
    path("", main_view, name="main"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("products/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("products/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
]
