from django.contrib import admin

from send.models import Recipient


# Register your models here.
@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'comment')
    list_filter = ('email',)
    search_fields = ('email', 'name',)
