from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("send/", include("send.urls", namespace="send")),
    path("users/", include("users.urls", namespace="users")),
]
