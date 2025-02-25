from django.urls import path

from send.apps import SendConfig
from send.views import RecipientCreateView, RecipientListView, main_view, RecipientUpdateView, RecipientDetailView, \
    RecipientDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, NewsletterDeleteView, \
    NewsletterBlockView, AttemptToSendCreateView, AttemptToSendListView

app_name = SendConfig.name

urlpatterns = [
    path("", main_view, name="main"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipients/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("newsletters/", NewsletterListView.as_view(), name="newsletter_list"),
    path("newsletters/<int:pk>/", NewsletterDetailView.as_view(), name="newsletter_detail"),
    path("newsletters/create/", NewsletterCreateView.as_view(), name="newsletter_create"),
    path("newsletters/<int:pk>/update/", NewsletterUpdateView.as_view(), name="newsletter_update"),
    path("newsletters/<int:pk>/block/", NewsletterBlockView.as_view(), name="newsletter_block"),
    path("newsletters/<int:pk>/delete/", NewsletterDeleteView.as_view(), name="newsletter_delete"),
    path("attempttosend/", AttemptToSendListView.as_view(), name="attempttosend_list"),
    # path("attempttosend/create/", AttemptToSendCreateView.as_view(), name="attempttosend_create"),
]
