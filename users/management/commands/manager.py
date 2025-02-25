from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from users.models import CustomUser


class Command(BaseCommand):
    help = 'Add group manager'

    def handle(self, *args, **kwargs):
        # Создаем новую группу «Менеджеры»
        # manager_group = Group.objects.create(name='manager')
        manager_group, _ = Group.objects.get_or_create(name='manager')

        # Получаем разрешения
        view_recipient = Permission.objects.get(codename='can_view_recipient')
        view_message = Permission.objects.get(codename='can_view_message')
        view_newsletter = Permission.objects.get(codename='can_view_newsletter')
        view_user = Permission.objects.get(codename='can_view_user')

        # Назначаем разрешения группе
        manager_group.permissions.add(view_recipient, view_message, view_newsletter, view_user)
        self.stdout.write(self.style.SUCCESS(f'Группа manager создана'))

        # Получаем пользователя
        if not CustomUser.objects.filter(email="admin@sky.com").exists():
            user = CustomUser.objects.create(email="admin@sky.com")
            user.set_password("12345")
            user.is_active = True
            user.save()
            user.groups.add(manager_group)
            self.stdout.write(self.style.SUCCESS(f'Создан менеджер с email {user.email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Менеджер существует!'))
