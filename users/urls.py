from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, UserDetailView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name='login'),
    path("logout/", LogoutView.as_view(template_name="login.html"), name='logout'),
    path("register/", UserCreateView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name='email-confirm'),
    path("<int:pk>/", UserDetailView.as_view(), name="detail"),
    # path("recipients/create/", RecipientCreateView.as_view(), name="recipient_create"),
    # path("products/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    # path("products/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
]
