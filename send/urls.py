from django.urls import path

from send.apps import SendConfig
from send.views import RecipientCreateView, RecipientListView

app_name = SendConfig.name

urlpatterns = [
    path("", RecipientListView.as_view(), name="recipient_list"),
    # path("<int:id>/", ProductCategoryListView.as_view(), name="product_category_list"),
    # path("products/<int:pk>/", cache_page(60)(ProductDetailView.as_view()), name="product_detail"),
    path("create/", RecipientCreateView.as_view(), name="recipient_create"),
    # path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    # path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]